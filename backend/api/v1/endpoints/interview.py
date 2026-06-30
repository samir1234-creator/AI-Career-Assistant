"""
Interview API Endpoints (Phase 8)
==================================
All interview-related API routes: session management, question generation,
answer evaluation, feedback, history, career coach, and gamification.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from api.v1.endpoints.user import get_current_user
from core.response import BaseResponse
from core.exceptions import AppException
from core.database import (
    create_interview_session, get_interview_sessions, get_interview_session_by_id,
    save_interview_answer, get_interview_answers, complete_interview_session,
    get_interview_stats, save_career_coach_message, get_career_coach_history,
    award_interview_badge, get_interview_badges, get_dashboard_summary
)
from services.interview_service import (
    InterviewService, EvaluationEngine, FeedbackEngine, CareerCoachEngine
)
from services.interview_question_bank import check_badge_eligibility

router = APIRouter()


# ─────────────────────────────────────────────────────────────
# REQUEST SCHEMAS
# ─────────────────────────────────────────────────────────────

class StartSessionRequest(BaseModel):
    interview_type: str = Field(..., description="mock | technical | hr | behavioral | coding | company")
    role: Optional[str] = Field(None, description="Target role (for mock interviews)")
    difficulty: Optional[str] = Field("Intermediate", description="Beginner | Intermediate | Advanced | Expert")
    company: Optional[str] = Field(None, description="Company name (for company-specific interviews)")
    topics: Optional[List[str]] = Field(default_factory=list, description="Topics for technical/coding")
    count: Optional[int] = Field(8, ge=1, le=15, description="Number of questions")
    resume_data: Optional[Dict[str, Any]] = Field(None, description="Resume data for personalized questions")

class EvaluateAnswerRequest(BaseModel):
    session_id: str
    question_index: int
    question_text: str
    question_type: Optional[str] = "general"
    answer_text: str
    time_taken_secs: Optional[int] = 0

class CompleteSessionRequest(BaseModel):
    session_id: str
    duration_seconds: Optional[int] = 0

class CodingSubmitRequest(BaseModel):
    session_id: str
    question_index: int
    question_text: str
    solution_text: str
    language: Optional[str] = "python"
    time_taken_secs: Optional[int] = 0
    hints_used: Optional[int] = 0

class CareerCoachRequest(BaseModel):
    message: str = Field(..., min_length=5, max_length=2000)


# ─────────────────────────────────────────────────────────────
# MODULE 1-6: QUESTION GENERATION & SESSION START
# ─────────────────────────────────────────────────────────────

@router.post("/start", response_model=BaseResponse[Dict[str, Any]])
async def start_interview_session(
    payload: StartSessionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Start a new interview session and generate questions."""
    try:
        user_id = str(current_user["id"])
        itype = payload.interview_type
        count = payload.count or 8

        # Generate questions based on type
        if itype == "mock":
            if not payload.role:
                raise HTTPException(status_code=400, detail="Role is required for mock interviews.")
            session_data = InterviewService.generate_mock_interview(payload.role, payload.difficulty or "Intermediate", count)
        elif itype == "resume_based":
            raise HTTPException(status_code=400, detail="Resume-based interviews are no longer supported.")
        elif itype == "technical":
            topics = payload.topics or ["Data Structures", "Algorithms"]
            session_data = InterviewService.generate_technical_interview(topics, payload.difficulty or "Intermediate", count)
        elif itype == "hr":
            session_data = InterviewService.generate_hr_interview(count)
        elif itype == "behavioral":
            session_data = InterviewService.generate_behavioral_interview(count)
        elif itype == "coding":
            topics = payload.topics or ["Arrays", "Strings"]
            diff = payload.difficulty or "Medium"
            session_data = InterviewService.generate_coding_interview(topics, diff, min(count, 5))
        elif itype == "company":
            if not payload.company:
                raise HTTPException(status_code=400, detail="Company is required for company-specific interviews.")
            session_data = InterviewService.generate_company_interview(payload.company, count)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown interview type: {itype}")

        # Persist session to DB
        session_id = create_interview_session(
            user_id=user_id,
            interview_type=itype,
            role=payload.role,
            difficulty=payload.difficulty,
            company=payload.company,
            topics=payload.topics or [],
            total_questions=session_data["total_questions"]
        )

        session_data["session_id"] = session_id
        return BaseResponse(success=True, data=session_data, message="Interview session started.")

    except HTTPException:
        raise
    except Exception as e:
        raise AppException(message=f"Failed to start interview session: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 7: ANSWER EVALUATION
# ─────────────────────────────────────────────────────────────

@router.post("/answer/evaluate", response_model=BaseResponse[Dict[str, Any]])
async def evaluate_answer(
    payload: EvaluateAnswerRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Evaluate a single interview answer and save it to the session."""
    try:
        user_id = str(current_user["id"])

        # Evaluate with scoring engine
        evaluation = EvaluationEngine.evaluate_answer(
            question=payload.question_text,
            answer=payload.answer_text,
            interview_type=payload.question_type or "general"
        )

        # Save to DB
        save_interview_answer(
            session_id=payload.session_id,
            user_id=user_id,
            question_index=payload.question_index,
            question_text=payload.question_text,
            question_type=payload.question_type or "general",
            answer_text=payload.answer_text,
            time_taken_secs=payload.time_taken_secs or 0,
            scores=evaluation["scores"],
            feedback=evaluation["feedback"]
        )

        return BaseResponse(success=True, data=evaluation, message="Answer evaluated.")

    except Exception as e:
        raise AppException(message=f"Evaluation failed: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 6: CODING CHALLENGE SUBMISSION
# ─────────────────────────────────────────────────────────────

@router.post("/coding/submit", response_model=BaseResponse[Dict[str, Any]])
async def submit_coding_solution(
    payload: CodingSubmitRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Evaluate a coding challenge solution (approach-based evaluation)."""
    try:
        user_id = str(current_user["id"])

        # Evaluate the coding solution as a general answer with coding context
        question_for_eval = f"[Coding Challenge]\n{payload.question_text}"
        answer_with_hints = payload.solution_text
        if payload.hints_used and payload.hints_used > 0:
            answer_with_hints += f"\n[Note: {payload.hints_used} hints used]"

        evaluation = EvaluationEngine.evaluate_answer(
            question=question_for_eval,
            answer=answer_with_hints,
            interview_type="coding"
        )

        # Adjust scores for coding context
        code_quality_bonus = 0
        sol_lower = payload.solution_text.lower()
        code_indicators = ["def ", "function", "class ", "for ", "while ", "if ", "return ", "->", "=>", "var ", "int ", "void "]
        code_count = sum(1 for ci in code_indicators if ci in sol_lower)
        if code_count >= 3:
            code_quality_bonus = 10

        evaluation["scores"]["technical_accuracy"] = min(100, evaluation["scores"]["technical_accuracy"] + code_quality_bonus)
        evaluation["overall_score"] = min(100, evaluation["overall_score"] + code_quality_bonus // 2)

        save_interview_answer(
            session_id=payload.session_id,
            user_id=user_id,
            question_index=payload.question_index,
            question_text=payload.question_text,
            question_type="coding",
            answer_text=payload.solution_text,
            time_taken_secs=payload.time_taken_secs or 0,
            scores=evaluation["scores"],
            feedback=evaluation["feedback"]
        )

        return BaseResponse(success=True, data=evaluation, message="Coding solution evaluated.")

    except Exception as e:
        raise AppException(message=f"Coding evaluation failed: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 8: SESSION COMPLETION & FEEDBACK
# ─────────────────────────────────────────────────────────────

@router.post("/session/complete", response_model=BaseResponse[Dict[str, Any]])
async def complete_session(
    payload: CompleteSessionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Complete an interview session and generate comprehensive feedback."""
    try:
        user_id = str(current_user["id"])

        # Fetch session details
        session = get_interview_session_by_id(payload.session_id, user_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found.")

        # Fetch all answers
        answers = get_interview_answers(payload.session_id, user_id)
        
        # Convert DB rows to evaluation format
        evaluated_answers = []
        for a in answers:
            scores = a.get("scores") or {}
            if isinstance(scores, str):
                import json
                scores = json.loads(scores)
            evaluated_answers.append({
                "question_text": a["question_text"],
                "answer_text": a.get("answer_text", ""),
                "scores": scores,
                "feedback": a.get("feedback", {}),
                "evaluated": a.get("evaluated", False),
                "overall_score": scores.get("overall", sum(scores.values()) / max(1, len(scores)) if scores else 0)
            })

        # Generate session feedback
        feedback = FeedbackEngine.generate_session_feedback(
            session_answers=evaluated_answers,
            interview_type=session.get("interview_type", "general"),
            role=session.get("role")
        )

        # Calculate overall session score
        overall = feedback.get("overall_score", 0)

        # Update session in DB
        complete_interview_session(
            session_id=payload.session_id,
            user_id=user_id,
            overall_score=overall,
            duration_seconds=payload.duration_seconds or 0,
            session_feedback=feedback
        )

        # Check and award badges
        stats = get_interview_stats(user_id)
        existing_badges = [b["badge_id"] for b in get_interview_badges(user_id)]
        
        # Enrich stats for badge check
        stats["has_ai_engineer_session"] = session.get("role") == "AI Engineer"
        stats["best_technical_score"] = stats.get("best_score", 0) if session.get("interview_type") == "technical" else 0
        stats["best_hr_score"] = stats.get("best_score", 0) if session.get("interview_type") == "hr" else 0
        stats["high_comm_sessions"] = 0
        stats["streak_days"] = 1

        new_badges = check_badge_eligibility(stats, existing_badges)
        awarded = []
        for badge in new_badges:
            if award_interview_badge(user_id, badge):
                awarded.append(badge)

        return BaseResponse(
            success=True,
            data={
                "session_id": payload.session_id,
                "overall_score": overall,
                "feedback": feedback,
                "new_badges": awarded,
                "answers_count": len(evaluated_answers)
            },
            message="Session completed with feedback."
        )

    except HTTPException:
        raise
    except Exception as e:
        raise AppException(message=f"Failed to complete session: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 9: INTERVIEW HISTORY
# ─────────────────────────────────────────────────────────────

@router.get("/sessions", response_model=BaseResponse[List[Dict[str, Any]]])
async def list_sessions(
    limit: int = 20,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List user's interview session history."""
    try:
        sessions = get_interview_sessions(str(current_user["id"]), limit)
        return BaseResponse(success=True, data=sessions, message="Sessions retrieved.")
    except Exception as e:
        raise AppException(message=f"Failed to fetch sessions: {str(e)}", status_code=500)


@router.get("/sessions/{session_id}", response_model=BaseResponse[Dict[str, Any]])
async def get_session_detail(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed session with all questions and answers."""
    try:
        user_id = str(current_user["id"])
        session = get_interview_session_by_id(session_id, user_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found.")
        
        answers = get_interview_answers(session_id, user_id)
        session["answers"] = answers
        
        return BaseResponse(success=True, data=session, message="Session details retrieved.")
    except HTTPException:
        raise
    except Exception as e:
        raise AppException(message=f"Failed to fetch session details: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 12: INTERVIEW DASHBOARD STATS
# ─────────────────────────────────────────────────────────────

@router.get("/stats", response_model=BaseResponse[Dict[str, Any]])
async def get_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get comprehensive interview statistics for the dashboard."""
    try:
        user_id = str(current_user["id"])
        stats = get_interview_stats(user_id)
        badges = get_interview_badges(user_id)
        
        # Determine readiness level
        total = stats.get("total_completed", 0)
        avg = float(stats.get("avg_score", 0))
        
        if total == 0:
            readiness = "Not Started"
            readiness_pct = 0
        elif total < 3 or avg < 50:
            readiness = "Beginner"
            readiness_pct = 20
        elif total < 10 or avg < 65:
            readiness = "Developing"
            readiness_pct = 45
        elif total < 20 or avg < 75:
            readiness = "Intermediate"
            readiness_pct = 65
        elif avg < 85:
            readiness = "Advanced"
            readiness_pct = 80
        else:
            readiness = "Interview Ready"
            readiness_pct = 95

        return BaseResponse(
            success=True,
            data={
                **stats,
                "badges": badges,
                "readiness": readiness,
                "readiness_pct": readiness_pct,
                "total_badges": len(badges),
            },
            message="Stats retrieved."
        )
    except Exception as e:
        raise AppException(message=f"Failed to fetch stats: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 11: CAREER COACH
# ─────────────────────────────────────────────────────────────

@router.post("/career-coach/ask", response_model=BaseResponse[Dict[str, Any]])
async def ask_career_coach(
    payload: CareerCoachRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Ask the AI Career Coach a question with full user context."""
    try:
        user_id = str(current_user["id"])

        # Build rich user context
        try:
            dashboard = get_dashboard_summary(user_id)
        except Exception:
            dashboard = {}

        # Extract resume from history
        history = dashboard.get("history", [])
        resume_data = {}
        if history:
            latest = history[0] if history else {}
            parsed = latest.get("parsed_data") or {}
            if isinstance(parsed, str):
                import json
                try:
                    parsed = json.loads(parsed)
                except Exception:
                    parsed = {}
            resume_data = parsed

        stats = get_interview_stats(user_id)
        profile = dashboard.get("profile", {})
        progress = dashboard.get("progress", {})

        user_context = {
            "resume": resume_data,
            "ats_score": profile.get("current_readiness_score", 0) or 0,
            "career_goal": profile.get("current_career_goal") or current_user.get("current_career_goal") or "",
            "roadmap_progress": progress.get("roadmap_progress", 0) or 0,
            "interview_stats": {
                "total_completed": int(stats.get("total_completed", 0)),
                "avg_score": float(stats.get("avg_score", 0)),
                "best_score": float(stats.get("best_score", 0)),
            },
        }

        # Generate response
        response_text = CareerCoachEngine.get_response(payload.message, user_context)

        # Save conversation
        save_career_coach_message(
            user_id=user_id,
            message=payload.message,
            response=response_text,
            context_used={
                "career_goal": user_context["career_goal"],
                "ats_score": user_context["ats_score"],
                "roadmap_progress": user_context["roadmap_progress"],
            }
        )

        return BaseResponse(
            success=True,
            data={"response": response_text, "timestamp": __import__("datetime").datetime.utcnow().isoformat()},
            message="Career coach response generated."
        )

    except Exception as e:
        raise AppException(message=f"Career coach error: {str(e)}", status_code=500)


@router.get("/career-coach/history", response_model=BaseResponse[List[Dict[str, Any]]])
async def get_coach_history(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Fetch career coach conversation history."""
    try:
        history = get_career_coach_history(str(current_user["id"]))
        return BaseResponse(success=True, data=history, message="History retrieved.")
    except Exception as e:
        raise AppException(message=f"Failed to fetch coach history: {str(e)}", status_code=500)


# ─────────────────────────────────────────────────────────────
# MODULE 13: BADGES
# ─────────────────────────────────────────────────────────────

@router.get("/badges", response_model=BaseResponse[List[Dict[str, Any]]])
async def get_badges(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all interview badges earned by the user."""
    try:
        badges = get_interview_badges(str(current_user["id"]))
        return BaseResponse(success=True, data=badges, message="Badges retrieved.")
    except Exception as e:
        raise AppException(message=f"Failed to fetch badges: {str(e)}", status_code=500)
