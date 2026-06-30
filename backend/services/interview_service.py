"""
Interview Service
=================
Core engine for generating interview questions, evaluating answers,
generating feedback, and providing career coaching responses.
Uses an intelligent rule-based scoring engine (no external LLM required).
"""

import re
import math
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.interview_question_bank import (
    get_role_questions, get_hr_questions, get_behavioral_questions,
    get_technical_questions, get_coding_challenges, get_company_questions,
    check_badge_eligibility,
    ROLE_QUESTIONS, COMPANY_PROFILES, INTERVIEW_BADGE_CATALOG
)


# ─────────────────────────────────────────────────────────────
# QUESTION GENERATION
# ─────────────────────────────────────────────────────────────

class InterviewService:

    @staticmethod
    def generate_mock_interview(role: str, difficulty: str, count: int = 8) -> Dict[str, Any]:
        """Generate a complete mock interview session config."""
        questions = get_role_questions(role, difficulty, count)
        
        # Enrich with metadata
        enriched = []
        for i, q in enumerate(questions):
            enriched.append({
                "id": f"q_{i+1}",
                "text": q["q"],
                "hint": q.get("hint", ""),
                "type": "mock",
                "time_limit": _get_time_limit(difficulty),
                "index": i + 1,
                "total": len(questions)
            })
        
        return {
            "role": role,
            "difficulty": difficulty,
            "interview_type": "mock",
            "questions": enriched,
            "total_questions": len(enriched),
            "estimated_duration_min": len(enriched) * _get_time_limit(difficulty) // 60 + 5
        }

    @staticmethod
    def generate_technical_interview(topics: List[str], difficulty: str, count: int = 10) -> Dict[str, Any]:
        """Generate technical interview questions."""
        questions = get_technical_questions(topics, difficulty, count)
        
        enriched = []
        for i, q in enumerate(questions):
            enriched.append({
                "id": f"q_{i+1}",
                "text": q["q"],
                "hint": "Think out loud — explain your reasoning step by step.",
                "type": "technical",
                "difficulty": q.get("difficulty", difficulty),
                "time_limit": _get_time_limit(difficulty),
                "index": i + 1,
                "total": len(questions)
            })
        
        return {
            "interview_type": "technical",
            "topics": topics,
            "difficulty": difficulty,
            "questions": enriched,
            "total_questions": len(enriched),
            "estimated_duration_min": len(enriched) * _get_time_limit(difficulty) // 60 + 5
        }

    @staticmethod
    def generate_hr_interview(count: int = 12) -> Dict[str, Any]:
        """Generate HR interview questions."""
        questions = get_hr_questions(count)
        
        enriched = []
        for i, q in enumerate(questions):
            enriched.append({
                "id": f"q_{i+1}",
                "text": q["q"],
                "hint": q.get("hint", "Be authentic and provide specific examples."),
                "category": q.get("category", "General"),
                "type": "hr",
                "time_limit": 120,
                "index": i + 1,
                "total": len(questions)
            })
        
        return {
            "interview_type": "hr",
            "questions": enriched,
            "total_questions": len(enriched),
            "estimated_duration_min": len(enriched) * 2 + 5
        }

    @staticmethod
    def generate_behavioral_interview(count: int = 8) -> Dict[str, Any]:
        """Generate behavioral (STAR format) interview questions."""
        questions = get_behavioral_questions(count)
        
        enriched = []
        for i, q in enumerate(questions):
            enriched.append({
                "id": f"q_{i+1}",
                "text": q["q"],
                "hint": "Use the STAR format: Situation → Task → Action → Result",
                "competency": q.get("competency", "General"),
                "type": "behavioral",
                "time_limit": 180,
                "index": i + 1,
                "total": len(questions),
                "star_guide": {
                    "situation": "Describe the context and challenge",
                    "task": "What was your specific role?",
                    "action": "What specific actions did you take?",
                    "result": "What was the outcome? Quantify if possible."
                }
            })
        
        return {
            "interview_type": "behavioral",
            "questions": enriched,
            "total_questions": len(enriched),
            "estimated_duration_min": len(enriched) * 3 + 5
        }

    @staticmethod
    def generate_coding_interview(topics: List[str], difficulty: str, count: int = 3) -> Dict[str, Any]:
        """Generate coding challenges."""
        challenges = get_coding_challenges(topics, difficulty, count)
        
        enriched = []
        for i, c in enumerate(challenges):
            enriched.append({
                "id": f"c_{i+1}",
                "title": c["title"],
                "text": c["problem"],
                "topic": c["topic"],
                "difficulty": c["difficulty"],
                "hints": c.get("hints", []),
                "approach": c.get("approach", ""),
                "time_complexity": c.get("time_complexity", ""),
                "space_complexity": c.get("space_complexity", ""),
                "type": "coding",
                "time_limit": _get_coding_time_limit(c["difficulty"]),
                "index": i + 1,
                "total": len(challenges)
            })
        
        return {
            "interview_type": "coding",
            "topics": topics,
            "difficulty": difficulty,
            "questions": enriched,
            "total_questions": len(enriched),
            "estimated_duration_min": len(enriched) * (_get_coding_time_limit(difficulty) // 60) + 5
        }

    @staticmethod
    def generate_company_interview(company: str, count: int = 6) -> Dict[str, Any]:
        """Generate company-specific interview."""
        profile = get_company_questions(company, count)
        
        questions_raw = profile.get("questions", [])
        enriched = []
        for i, q in enumerate(questions_raw):
            q_text = q.get("q", q) if isinstance(q, dict) else str(q)
            q_type = q.get("type", "general") if isinstance(q, dict) else "general"
            enriched.append({
                "id": f"q_{i+1}",
                "text": q_text,
                "type": q_type,
                "hint": q.get("lp", "") if isinstance(q, dict) else "",
                "time_limit": 180,
                "index": i + 1,
                "total": len(questions_raw)
            })
        
        return {
            "interview_type": "company",
            "company": company,
            "style": profile.get("style", ""),
            "focus_areas": profile.get("focus_areas", []),
            "difficulty": profile.get("difficulty", "Intermediate"),
            "questions": enriched,
            "total_questions": len(enriched),
            "estimated_duration_min": len(enriched) * 3 + 10
        }


# ─────────────────────────────────────────────────────────────
# ANSWER EVALUATION ENGINE
# ─────────────────────────────────────────────────────────────

class EvaluationEngine:

    @staticmethod
    def evaluate_answer(question: str, answer: str, interview_type: str = "general") -> Dict[str, Any]:
        """
        Evaluate a user's answer across 6 dimensions using intelligent
        rule-based analysis. Returns detailed scores and feedback.
        """
        if not answer or len(answer.strip()) < 10:
            return _empty_answer_response()
        
        answer_clean = answer.strip()
        words = answer_clean.split()
        word_count = len(words)
        sentences = [s.strip() for s in re.split(r'[.!?]+', answer_clean) if s.strip()]
        sentence_count = max(1, len(sentences))
        
        # ── 1. Technical Accuracy ────────────────────────────────────────
        tech_score = _evaluate_technical_accuracy(question, answer_clean, interview_type, word_count)
        
        # ── 2. Communication ─────────────────────────────────────────────
        comm_score = _evaluate_communication(answer_clean, word_count, sentence_count)
        
        # ── 3. Grammar ───────────────────────────────────────────────────
        grammar_score = _evaluate_grammar(answer_clean, word_count)
        
        # ── 4. Confidence ────────────────────────────────────────────────
        confidence_score = _evaluate_confidence(answer_clean)
        
        # ── 5. Completeness ──────────────────────────────────────────────
        completeness_score = _evaluate_completeness(question, answer_clean, word_count, interview_type)
        
        # ── 6. Professionalism ───────────────────────────────────────────
        professionalism_score = _evaluate_professionalism(answer_clean, word_count)
        
        # ── Overall Score (weighted) ─────────────────────────────────────
        weights = {
            "technical_accuracy": 0.30,
            "completeness": 0.25,
            "communication": 0.20,
            "confidence": 0.10,
            "grammar": 0.10,
            "professionalism": 0.05,
        }
        
        scores = {
            "technical_accuracy": tech_score,
            "communication": comm_score,
            "grammar": grammar_score,
            "confidence": confidence_score,
            "completeness": completeness_score,
            "professionalism": professionalism_score,
        }
        
        overall = sum(scores[k] * weights[k] for k in weights)
        overall = round(min(100, max(0, overall)))
        
        # ── Generate Feedback ────────────────────────────────────────────
        feedback = _generate_answer_feedback(
            question, answer_clean, scores, overall, interview_type, word_count
        )
        
        return {
            "scores": {k: round(v) for k, v in scores.items()},
            "overall_score": overall,
            "rating": _score_to_rating(overall),
            "word_count": word_count,
            "feedback": feedback,
        }


# ─────────────────────────────────────────────────────────────
# SESSION FEEDBACK GENERATOR
# ─────────────────────────────────────────────────────────────

class FeedbackEngine:

    @staticmethod
    def generate_session_feedback(session_answers: List[Dict[str, Any]], interview_type: str, role: str = None) -> Dict[str, Any]:
        """Generate comprehensive feedback for a completed interview session."""
        if not session_answers:
            return _empty_session_feedback()
        
        evaluated = [a for a in session_answers if a.get("evaluated") and a.get("scores")]
        if not evaluated:
            return _empty_session_feedback()
        
        # Aggregate scores
        score_keys = ["technical_accuracy", "communication", "grammar", "confidence", "completeness", "professionalism"]
        avg_scores = {}
        for key in score_keys:
            vals = [a["scores"].get(key, 0) for a in evaluated if a.get("scores")]
            avg_scores[key] = round(sum(vals) / len(vals)) if vals else 0
        
        overall_scores = [a.get("overall_score", 0) for a in evaluated]
        avg_overall = round(sum(overall_scores) / len(overall_scores)) if overall_scores else 0
        
        # Identify strengths (top 2 scoring dimensions)
        sorted_dims = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
        strengths = _dims_to_strengths(sorted_dims[:2])
        
        # Identify weaknesses (bottom 2 scoring dimensions)
        weaknesses = _dims_to_weaknesses(sorted_dims[-2:])
        
        # Missing topics from answers
        missing_topics = _identify_missing_topics(session_answers, role)
        
        # Concepts to revise
        concepts_to_revise = _get_concepts_to_revise(avg_scores, interview_type, role)
        
        # Learning resources
        resources = _get_recommended_resources(interview_type, role, avg_scores)
        
        # Practice problems
        practice = _get_practice_recommendations(interview_type, avg_overall)
        
        # Score trend within session
        score_trend = [a.get("overall_score", 0) for a in session_answers if a.get("overall_score")]
        
        return {
            "overall_score": avg_overall,
            "avg_scores": avg_scores,
            "rating": _score_to_rating(avg_overall),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing_topics": missing_topics,
            "concepts_to_revise": concepts_to_revise,
            "recommended_resources": resources,
            "practice_problems": practice,
            "score_trend": score_trend,
            "total_answered": len(evaluated),
            "improvement_priority": _get_improvement_priority(avg_scores),
        }


# ─────────────────────────────────────────────────────────────
# CAREER COACH ENGINE
# ─────────────────────────────────────────────────────────────

class CareerCoachEngine:

    @staticmethod
    def get_response(user_message: str, user_context: Dict[str, Any]) -> str:
        """
        Generate a career coaching response based on user message and context.
        Uses intent detection + context-aware templates.
        """
        msg_lower = user_message.lower()
        
        # Extract context
        resume = user_context.get("resume", {})
        ats_score = user_context.get("ats_score", 0)
        career_goal = user_context.get("career_goal", "")
        roadmap_progress = user_context.get("roadmap_progress", 0)
        interview_stats = user_context.get("interview_stats", {})
        skills = resume.get("skills", []) if resume else []
        skill_names = [s if isinstance(s, str) else s.get("name", "") for s in skills[:10]]
        
        # ── Intent Detection ─────────────────────────────────────────────
        
        # What to learn next
        if any(phrase in msg_lower for phrase in ["learn next", "what should i", "next step", "focus on", "study"]):
            return _coach_learn_next(career_goal, skill_names, roadmap_progress, interview_stats)
        
        # ATS improvement
        if any(phrase in msg_lower for phrase in ["ats", "resume score", "improve resume", "ats score"]):
            return _coach_ats_improvement(ats_score, skill_names, career_goal)
        
        # Projects to build
        if any(phrase in msg_lower for phrase in ["project", "build", "portfolio", "side project"]):
            return _coach_projects(career_goal, skill_names)
        
        # Certifications
        if any(phrase in msg_lower for phrase in ["certif", "course", "credential"]):
            return _coach_certifications(career_goal, skill_names)
        
        # Interview preparation
        if any(phrase in msg_lower for phrase in ["interview", "prepare", "practice", "mock"]):
            return _coach_interview_prep(career_goal, interview_stats, ats_score)
        
        # Job recommendations
        if any(phrase in msg_lower for phrase in ["job", "role", "position", "apply", "hiring"]):
            return _coach_jobs(career_goal, skill_names, ats_score)
        
        # Salary / negotiation
        if any(phrase in msg_lower for phrase in ["salary", "negotiat", "pay", "compensation"]):
            return _coach_salary(career_goal, skill_names)
        
        # Networking
        if any(phrase in msg_lower for phrase in ["network", "linkedin", "connect", "referral"]):
            return _coach_networking(career_goal)
        
        # Default comprehensive response
        return _coach_default(career_goal, ats_score, roadmap_progress, interview_stats, skill_names)


# ─────────────────────────────────────────────────────────────
# SCORING HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def _get_time_limit(difficulty: str) -> int:
    """Time limit in seconds per question."""
    return {"Beginner": 90, "Intermediate": 120, "Advanced": 180, "Expert": 240}.get(difficulty, 120)

def _get_coding_time_limit(difficulty: str) -> int:
    return {"Easy": 900, "Medium": 1800, "Hard": 2700}.get(difficulty, 1800)

def _score_to_rating(score: float) -> str:
    if score >= 90: return "Excellent"
    if score >= 80: return "Very Good"
    if score >= 70: return "Good"
    if score >= 60: return "Fair"
    if score >= 50: return "Needs Improvement"
    return "Poor"

def _empty_answer_response() -> Dict:
    return {
        "scores": {"technical_accuracy": 0, "communication": 0, "grammar": 0, "confidence": 0, "completeness": 0, "professionalism": 0},
        "overall_score": 0,
        "rating": "No Answer",
        "word_count": 0,
        "feedback": {"strengths": [], "improvements": ["Please provide a detailed answer to receive evaluation."], "suggestions": ["Write at least 3-5 sentences for meaningful evaluation."]},
    }

def _empty_session_feedback() -> Dict:
    return {
        "overall_score": 0, "avg_scores": {}, "rating": "Incomplete",
        "strengths": [], "weaknesses": [], "missing_topics": [],
        "concepts_to_revise": [], "recommended_resources": [], "practice_problems": [],
        "score_trend": [], "total_answered": 0, "improvement_priority": []
    }

def _evaluate_technical_accuracy(question: str, answer: str, interview_type: str, word_count: int) -> float:
    """Score technical depth and accuracy."""
    score = 50.0  # baseline
    
    # Length bonus (technical answers need substance)
    if word_count >= 100: score += 20
    elif word_count >= 60: score += 12
    elif word_count >= 30: score += 6
    elif word_count < 15: score -= 20
    
    # Technical keywords presence
    tech_terms = [
        "algorithm", "complexity", "o(n", "o(log", "time", "space", "memory", "performance",
        "architecture", "design", "pattern", "database", "api", "model", "layer", "framework",
        "function", "class", "method", "object", "interface", "async", "thread", "process",
        "neural", "training", "gradient", "loss", "epoch", "batch", "tensor", "vector",
        "cache", "queue", "stack", "tree", "graph", "hash", "index", "query", "transaction",
        "deploy", "scale", "load", "latency", "throughput", "bottleneck", "optimize",
    ]
    answer_lower = answer.lower()
    found_tech = sum(1 for term in tech_terms if term in answer_lower)
    score += min(15, found_tech * 2.5)
    
    # HR/behavioral doesn't need heavy tech scoring
    if interview_type in ("hr", "behavioral"):
        score = 60 + min(20, word_count // 5)
    
    # Mentions specific examples
    example_markers = ["for example", "for instance", "such as", "like", "i used", "i built", "i implemented", "we designed"]
    if any(m in answer_lower for m in example_markers):
        score += 8
    
    # Numbers/metrics (shows concreteness)
    numbers = re.findall(r'\b\d+[%x]?\b', answer)
    if len(numbers) >= 2: score += 7
    elif len(numbers) >= 1: score += 3
    
    return min(100, max(0, score))

def _evaluate_communication(answer: str, word_count: int, sentence_count: int) -> float:
    """Score clarity and structure of communication."""
    score = 50.0
    
    # Ideal length (150-400 words for spoken answers)
    if 100 <= word_count <= 400: score += 25
    elif 60 <= word_count < 100: score += 15
    elif 400 < word_count <= 600: score += 10
    elif word_count < 30: score -= 25
    
    # Structural markers
    structure_words = ["first", "second", "third", "finally", "moreover", "additionally",
                       "however", "therefore", "in conclusion", "to summarize", "overall",
                       "next", "then", "lastly", "importantly", "specifically"]
    answer_lower = answer.lower()
    structure_count = sum(1 for w in structure_words if w in answer_lower)
    score += min(15, structure_count * 4)
    
    # Avg sentence length (8-20 words is ideal)
    avg_sent_len = word_count / sentence_count
    if 8 <= avg_sent_len <= 20: score += 10
    elif avg_sent_len < 5 or avg_sent_len > 30: score -= 5
    
    return min(100, max(0, score))

def _evaluate_grammar(answer: str, word_count: int) -> float:
    """Score grammar quality (approximated via patterns)."""
    score = 75.0  # Default decent
    
    # Basic quality signals
    if word_count > 20: score += 5
    
    # Check for basic capitalization at sentence start
    sentences = re.split(r'[.!?]+\s+', answer.strip())
    well_capped = sum(1 for s in sentences if s and s[0].isupper())
    if sentences:
        cap_ratio = well_capped / len(sentences)
        score += 10 * cap_ratio
    
    # Repetitive filler words (penalty)
    filler_words = ["uh", "um", "like like", "you know", "basically basically"]
    filler_count = sum(answer.lower().count(f) for f in filler_words)
    score -= filler_count * 3
    
    # Very short responses tend to have poor grammar representation
    if word_count < 20: score -= 20
    
    return min(100, max(30, score))

def _evaluate_confidence(answer: str) -> float:
    """Score perceived confidence from language patterns."""
    score = 60.0
    answer_lower = answer.lower()
    
    # Confident language markers
    confident = ["i believe", "i am confident", "i have", "i worked", "i led", "i built",
                 "my approach", "my experience", "definitely", "certainly", "i know",
                 "i implemented", "we achieved", "i designed", "successfully"]
    conf_count = sum(1 for c in confident if c in answer_lower)
    score += min(25, conf_count * 5)
    
    # Uncertain language (penalty)
    uncertain = ["i think maybe", "i'm not sure", "i don't know", "perhaps maybe",
                 "i guess", "kind of", "sort of", "i might", "probably maybe"]
    unc_count = sum(1 for u in uncertain if u in answer_lower)
    score -= unc_count * 8
    
    # Hedging (small penalty — some hedging is OK)
    hedging = ["maybe", "perhaps", "i think", "i feel", "i believe maybe"]
    hedge_count = sum(1 for h in hedging if h in answer_lower)
    score -= min(15, hedge_count * 3)
    
    return min(100, max(20, score))

def _evaluate_completeness(question: str, answer: str, word_count: int, interview_type: str) -> float:
    """Score how completely the question was addressed."""
    score = 45.0
    
    # Length is a proxy for completeness
    if word_count >= 150: score += 30
    elif word_count >= 80: score += 20
    elif word_count >= 40: score += 10
    elif word_count < 20: score -= 20
    
    # STAR format completeness for behavioral
    if interview_type == "behavioral":
        star_markers = {
            "situation": ["situation", "context", "working at", "when i"],
            "task": ["task", "responsibility", "role", "need to"],
            "action": ["i did", "i took", "i decided", "my action", "i implemented", "i proposed"],
            "result": ["result", "outcome", "achieved", "%", "increased", "reduced", "saved", "impact"],
        }
        star_hit = sum(1 for markers in star_markers.values() 
                      if any(m in answer.lower() for m in markers))
        score += star_hit * 6
    
    # Mentions trade-offs / alternatives (shows depth)
    tradeoff_markers = ["however", "trade-off", "on the other hand", "alternatively", "versus", "compared to", "pros", "cons"]
    if any(m in answer.lower() for m in tradeoff_markers):
        score += 10
    
    return min(100, max(0, score))

def _evaluate_professionalism(answer: str, word_count: int) -> float:
    """Score professional tone and presentation."""
    score = 70.0
    answer_lower = answer.lower()
    
    # Informal/unprofessional (penalty)
    informal = ["lol", "omg", "wtf", "gonna", "wanna", "kinda", "y'all", "sup", "dude", "awesome bro"]
    informal_count = sum(1 for i in informal if i in answer_lower)
    score -= informal_count * 10
    
    # Professional markers (bonus)
    professional = ["professional", "industry", "stakeholder", "business", "team", "organization",
                    "client", "deliver", "collaborate", "strategy", "best practice", "standard"]
    prof_count = sum(1 for p in professional if p in answer_lower)
    score += min(20, prof_count * 3)
    
    if word_count > 50: score += 5
    
    return min(100, max(30, score))

def _generate_answer_feedback(question: str, answer: str, scores: Dict, overall: float, interview_type: str, word_count: int) -> Dict:
    """Generate actionable feedback for a specific answer."""
    strengths = []
    improvements = []
    suggestions = []
    
    # Strengths based on high scores
    if scores["technical_accuracy"] >= 75:
        strengths.append("Strong technical knowledge demonstrated with relevant concepts")
    if scores["communication"] >= 75:
        strengths.append("Clear and well-structured communication")
    if scores["confidence"] >= 75:
        strengths.append("Confident and assertive delivery")
    if scores["completeness"] >= 75:
        strengths.append("Comprehensive answer covering all key aspects")
    if word_count >= 100:
        strengths.append("Good answer length with sufficient detail")
    
    # Improvements based on low scores
    if scores["technical_accuracy"] < 60:
        improvements.append("Include more specific technical details, terminology, and examples")
        suggestions.append("Back up your answer with concrete technical examples or metrics")
    if scores["completeness"] < 60:
        improvements.append("Your answer could be more comprehensive — expand on key points")
        suggestions.append("Aim for 100-200 words; cover edge cases and trade-offs")
    if scores["communication"] < 60:
        improvements.append("Structure your answer more clearly (e.g., use 'First...', 'Then...', 'Finally...')")
        suggestions.append("Use transitional phrases to guide the interviewer through your thinking")
    if scores["confidence"] < 55:
        improvements.append("Use more confident, assertive language ('I implemented', 'I led', 'I designed')")
        suggestions.append("Avoid excessive hedging words like 'maybe', 'I guess', 'I think maybe'")
    if scores["grammar"] < 60:
        improvements.append("Review grammar and sentence structure before answering in interviews")
        suggestions.append("Practice writing out answers — it helps organize thoughts and improves grammar")
    
    # Interview-type specific suggestions
    if interview_type == "behavioral" and not any(m in answer.lower() for m in ["result", "outcome", "achieved"]):
        suggestions.append("Always end your STAR answer with quantifiable results: 'This resulted in X% improvement...'")
    
    if interview_type == "technical" and word_count < 50:
        suggestions.append("For technical questions, always explain the 'why' behind your approach, not just the 'what'")
    
    if not improvements:
        improvements.append("Continue refining your delivery for maximum impact")
    
    if not strengths:
        strengths.append("You made an attempt — keep practicing to build stronger answers")
    
    return {
        "strengths": strengths[:3],
        "improvements": improvements[:3],
        "suggestions": suggestions[:3],
    }


# ─────────────────────────────────────────────────────────────
# SESSION FEEDBACK HELPERS
# ─────────────────────────────────────────────────────────────

def _dims_to_strengths(top_dims: List) -> List[str]:
    dim_labels = {
        "technical_accuracy": "Strong technical knowledge and depth",
        "communication": "Clear and effective communication skills",
        "confidence": "Confident and assertive delivery",
        "completeness": "Comprehensive and detailed answers",
        "grammar": "Well-articulated and grammatically sound responses",
        "professionalism": "Professional tone and presentation",
    }
    return [dim_labels.get(d[0], d[0]) for d in top_dims if d[1] >= 60]

def _dims_to_weaknesses(bottom_dims: List) -> List[str]:
    dim_labels = {
        "technical_accuracy": "Technical depth needs improvement — add more specific examples and terminology",
        "communication": "Work on structuring answers with clearer transitions and organization",
        "confidence": "Build confidence — practice replacing uncertain language with assertive statements",
        "completeness": "Answers need to be more comprehensive — cover all aspects of the question",
        "grammar": "Practice articulating answers more clearly to improve grammar and fluency",
        "professionalism": "Maintain professional tone throughout — avoid informal language",
    }
    return [dim_labels.get(d[0], d[0]) for d in bottom_dims if d[1] < 75]

def _identify_missing_topics(answers: List[Dict], role: Optional[str]) -> List[str]:
    missing = []
    all_text = " ".join([a.get("answer_text", "") for a in answers]).lower()
    
    key_topics = {
        "examples": ["for example", "for instance", "specifically", "such as"],
        "metrics": ["%", "percent", "improved", "increased", "reduced", "times faster"],
        "trade-offs": ["trade-off", "however", "on the other hand", "alternatively", "vs"],
        "scalability": ["scale", "scalab", "million", "high traffic", "distribute"],
        "security": ["security", "auth", "encrypt", "secure", "vulnerab"],
    }
    
    for topic, markers in key_topics.items():
        if not any(m in all_text for m in markers):
            missing.append(topic.capitalize())
    
    return missing[:5]

def _get_concepts_to_revise(avg_scores: Dict, interview_type: str, role: Optional[str]) -> List[str]:
    concepts = []
    
    if avg_scores.get("technical_accuracy", 100) < 70:
        if interview_type == "technical":
            concepts.extend(["Data Structures & Algorithms", "System Design Principles", "Language-specific internals"])
        elif interview_type == "mock":
            concepts.extend([f"Core {role} technical concepts", "Industry best practices", "Common interview patterns"])
    
    if avg_scores.get("completeness", 100) < 70:
        concepts.append("STAR Method for structured answers")
        concepts.append("Quantifying impact with metrics")
    
    if avg_scores.get("communication", 100) < 70:
        concepts.append("Answer structuring techniques")
        concepts.append("Technical communication skills")
    
    concepts.extend(["Behavioral interview frameworks", "Common follow-up question patterns"])
    
    return list(dict.fromkeys(concepts))[:6]  # deduplicate

def _get_recommended_resources(interview_type: str, role: Optional[str], avg_scores: Dict) -> List[Dict]:
    resources = []
    
    # Always recommend
    resources.append({"title": "LeetCode 75 - Curated Problem List", "url": "https://leetcode.com/studyplan/leetcode-75/", "type": "Practice"})
    resources.append({"title": "System Design Interview Book (Vol 1)", "url": "https://www.amazon.com/System-Design-Interview/dp/B08CMF2CQF", "type": "Book"})
    resources.append({"title": "Grokking Modern System Design", "url": "https://www.educative.io/courses/grokking-modern-system-design-interview", "type": "Course"})
    
    if interview_type in ("hr", "behavioral"):
        resources.append({"title": "The STAR Interview Method Guide", "url": "https://www.themuse.com/advice/star-interview-method", "type": "Article"})
        resources.append({"title": "Amazon Leadership Principles Guide", "url": "https://www.amazon.jobs/en/principles", "type": "Reference"})
    
    if interview_type == "coding":
        resources.append({"title": "NeetCode - Structured DSA Learning", "url": "https://neetcode.io/", "type": "Practice"})
        resources.append({"title": "Blind 75 Problems", "url": "https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions", "type": "Practice"})
    
    if role and "AI" in role or "ML" in role if role else False:
        resources.append({"title": "ML Interview Book by Chip Huyen", "url": "https://huyenchip.com/ml-interviews-book/", "type": "Book"})
    
    return resources[:5]

def _get_practice_recommendations(interview_type: str, overall_score: float) -> List[str]:
    recs = []
    
    if overall_score < 60:
        recs.append("Practice daily: answer 5 questions out loud and record yourself")
        recs.append("Start with beginner difficulty and progressively increase")
    elif overall_score < 80:
        recs.append("Focus on intermediate questions in your weak areas")
        recs.append("Participate in mock interviews with a friend or mentor")
    else:
        recs.append("Move to expert-level questions to further sharpen your skills")
        recs.append("Practice whiteboard coding under time pressure")
    
    if interview_type == "coding":
        recs.extend(["Solve 2 LeetCode problems daily (1 easy, 1 medium)", "Practice explaining your solution approach before coding"])
    elif interview_type == "behavioral":
        recs.extend(["Prepare 10 STAR stories covering different competencies", "Practice concise delivery under 3 minutes per answer"])
    
    return recs[:4]

def _get_improvement_priority(avg_scores: Dict) -> List[str]:
    """Return dimensions sorted by priority of improvement."""
    sorted_dims = sorted(avg_scores.items(), key=lambda x: x[1])
    priority_map = {
        "technical_accuracy": "Technical Depth",
        "completeness": "Answer Completeness",
        "communication": "Communication Clarity",
        "confidence": "Confidence Level",
        "grammar": "Grammar & Fluency",
        "professionalism": "Professional Tone",
    }
    return [priority_map.get(d[0], d[0]) for d in sorted_dims[:3] if d[1] < 80]


# ─────────────────────────────────────────────────────────────
# CAREER COACH RESPONSE TEMPLATES
# ─────────────────────────────────────────────────────────────

def _coach_learn_next(career_goal: str, skills: List[str], roadmap_progress: float, interview_stats: Dict) -> str:
    goal = career_goal or "your career goal"
    progress = roadmap_progress or 0
    avg_score = interview_stats.get("avg_score", 0)
    
    if progress < 30:
        focus = "foundational skills"
        recs = "focus on building strong fundamentals: core programming, data structures, and algorithms."
    elif progress < 60:
        focus = "intermediate skills"
        recs = "move to intermediate concepts: system design, advanced frameworks, and real-world projects."
    else:
        focus = "advanced skills"
        recs = "sharpen advanced skills: distributed systems, performance optimization, and leadership."
    
    response = f"""Based on your profile targeting **{goal}**, here's what I recommend:

**Your Current Status:**
- Roadmap Progress: {progress:.0f}%
- Interview Avg Score: {avg_score:.0f}%
- Current Focus Area: {focus.title()}

**What to Learn Next:**
1. {recs}
2. {"Strengthen your interview skills — your scores show room for improvement." if avg_score < 70 else "Keep up your interview practice — you're performing well!"}
3. Build one real-world project that demonstrates end-to-end skills.

**Recommended Learning Order:**
- Complete your current roadmap milestone first
- Then tackle mock interviews in your target role at the next difficulty level
- Follow up with company-specific interview prep

Would you like specific resource recommendations or a detailed learning plan?"""
    
    return response

def _coach_ats_improvement(ats_score: float, skills: List[str], career_goal: str) -> str:
    score = ats_score or 0
    goal = career_goal or "your target role"
    
    if score >= 80:
        status = "excellent"
        action = "Your resume is ATS-optimized. Focus on tailoring the summary for specific job descriptions."
    elif score >= 60:
        status = "good"
        action = "A few targeted improvements can push your score higher."
    else:
        status = "needs improvement"
        action = "Significant improvements needed to pass ATS screening."
    
    return f"""Your ATS score is **{score:.0f}%** — {status}.

**{action}**

**Top ATS Improvement Strategies:**

1. **Keywords** — Add role-specific keywords from job descriptions. For {goal}, include terms like: {', '.join(skills[:5]) if skills else 'Python, APIs, cloud, data, system design'}

2. **Format** — Use a clean single-column format. Avoid tables, images, and graphics.

3. **Action Verbs** — Start bullets with: Built, Designed, Implemented, Led, Optimized, Reduced, Increased

4. **Quantification** — Add numbers: "Improved performance by 40%", "Built a system serving 10K users"

5. **Skills Section** — Create a dedicated, clear skills section that matches JD keywords exactly

6. **Job Title Match** — If your target is "AI Engineer", use that exact phrase in your current title/summary

**Quick Wins:**
- Re-upload your resume after adding 5-10 more relevant keywords
- Tailor your summary section for each application
- Add a "Technical Skills" section if missing"""

def _coach_projects(career_goal: str, skills: List[str]) -> str:
    goal = career_goal or "software engineering"
    
    project_ideas = {
        "AI Engineer": ["LLM-powered chatbot with RAG", "Image classification API with FastAPI", "Real-time sentiment analysis dashboard", "AI code review bot"],
        "Machine Learning Engineer": ["End-to-end ML pipeline with MLflow", "Fraud detection model with explainability", "Time series forecasting system", "Model serving API with monitoring"],
        "Full Stack Developer": ["Full-stack SaaS app with auth", "Real-time collaboration tool", "E-commerce platform with payment integration", "Social media analytics dashboard"],
        "Data Scientist": ["Predictive analytics dashboard", "NLP text classification tool", "Customer churn prediction system", "Interactive data visualization app"],
    }
    
    ideas = project_ideas.get(goal, ["RESTful API with authentication", "Full-stack CRUD app", "Data pipeline with visualization", "CLI tool that solves a real problem"])
    
    return f"""Based on your goal of becoming a **{goal}**, here are the most impactful projects to build:

**High-Impact Project Ideas:**
{chr(10).join(f"{i+1}. **{idea}** — demonstrates end-to-end skills" for i, idea in enumerate(ideas[:4]))}

**Project Building Strategy:**
1. Pick projects that showcase your **existing skills** ({', '.join(skills[:3]) if skills else 'your core skills'})
2. Deploy publicly on GitHub + a live URL (Vercel, Railway, or Heroku)
3. Write a detailed README: problem solved, architecture, tech stack, installation
4. Include tests to show engineering maturity
5. Create a demo video for LinkedIn

**What Recruiters Look For:**
- Live deployed app (not just code)
- Clear problem statement and solution
- Architecture documentation
- Contribution to open source

**Your Next Project:** I recommend starting with "{ideas[0]}" — it directly aligns with your target role and showcases skills recruiters actively search for."""

def _coach_certifications(career_goal: str, skills: List[str]) -> str:
    goal = career_goal or "your field"
    
    cert_map = {
        "AI Engineer": [("Google Professional ML Engineer", "High value, 4-6 months prep"), ("AWS Certified ML Specialty", "Industry recognized"), ("TensorFlow Developer Certificate", "Affordable, 2-3 months")],
        "Cloud Engineer": [("AWS Solutions Architect Associate", "Most in-demand cloud cert"), ("Google Cloud Professional Architect", "Growing demand"), ("Azure Administrator Associate", "Strong in enterprise")],
        "Data Scientist": [("Google Data Analytics Certificate", "Good entry-level"), ("IBM Data Science Professional", "Comprehensive"), ("Databricks Certified Associate", "Big data focused")],
        "DevOps Engineer": [("Certified Kubernetes Administrator (CKA)", "High demand"), ("AWS DevOps Professional", "Strong salary uplift"), ("HashiCorp Terraform Associate", "IaC credential")],
    }
    
    certs = cert_map.get(goal, [
        ("AWS Cloud Practitioner", "Great starting cert, 2-4 weeks"),
        ("Google IT Support Certificate", "Entry-level, beginner-friendly"),
        ("CompTIA Security+", "Broad security credential"),
    ])
    
    return f"""Here are the most valuable certifications for **{goal}**:

**Top Certifications by ROI:**
{chr(10).join(f"{i+1}. **{cert[0]}** — {cert[1]}" for i, cert in enumerate(certs))}

**Certification Strategy:**
- Start with 1 cert, not multiple simultaneously
- Choose platforms: Coursera, A Cloud Guru, Linux Foundation, or official vendor prep
- Budget for exam vouchers (usually $150-$400)
- Practice with free tier of the cloud platform

**Which to prioritize:**
For your goal of {goal}, I recommend starting with **{certs[0][0]}** — it has the best ROI and is immediately recognized by recruiters.

**Free Study Resources:**
- Official vendor documentation (AWS/GCP/Azure all offer free training)
- YouTube channels: freeCodeCamp, TechWorld with Nana, NetworkChuck
- Practice exams: Whizlabs, ExamPro, or Udemy dumps"""

def _coach_interview_prep(career_goal: str, interview_stats: Dict, ats_score: float) -> str:
    goal = career_goal or "your target role"
    total = interview_stats.get("total_completed", 0)
    avg_score = interview_stats.get("avg_score", 0)
    
    return f"""Here's your personalized interview preparation plan for **{goal}**:

**Your Interview Stats:**
- Sessions Completed: {total}
- Average Score: {avg_score:.0f}%
- ATS Score: {ats_score:.0f}%

**3-Phase Preparation Plan:**

**Phase 1 — Foundation (Weeks 1-2)**
- Complete 3 HR interview sessions (aim for 80%+)
- Practice "Tell me about yourself" daily until perfect
- Prepare 10 STAR stories covering: leadership, conflict, failure, achievement

**Phase 2 — Technical (Weeks 3-4)**  
- Solve 5 LeetCode problems per week (Easy + Medium)
- Complete 2 technical interview sessions per week
- Study system design: design 1 system per day
- Review your weak topics from interview feedback

**Phase 3 — Company-Specific (Week 5+)**
- Research your target companies' interview styles
- Complete company-specific mock interviews
- Practice behavioral questions aligned to company values
- Schedule real applications alongside practice

**Daily Habit:** 
30 min LeetCode + 1 mock question answered out loud = fastest improvement.

Ready to start? Go to the Interview Center and begin a session!"""

def _coach_jobs(career_goal: str, skills: List[str], ats_score: float) -> str:
    goal = career_goal or "tech"
    score = ats_score or 0
    
    readiness = "ready" if score >= 70 else "nearly ready" if score >= 50 else "in preparation"
    
    return f"""Based on your profile, here's job search guidance for **{goal}**:

**Your Job Readiness:** {readiness.title()} (ATS Score: {score:.0f}%)

**Best Job Platforms for {goal}:**
1. **LinkedIn** — Set job alerts, apply within 24 hours of posting
2. **Glassdoor** — Research company culture and salaries
3. **Indeed** — High volume, good for entry-mid level
4. **AngelList/Wellfound** — Startups with equity
5. **Hired.com** — Tech-specific, companies reach out to you

**Application Strategy:**
- Apply to 5-10 positions per week (quality > quantity)
- Tailor your resume for each application (15 min of keyword matching)
- Apply within 3 days of posting for best chance
- Set up LinkedIn "Open to Work" (visible to recruiters only option available)

**Skills that boost your profile:** {', '.join(skills[:5]) if skills else 'expand your technical skills'}

**Referral Strategy (2x success rate):**
- Message 5 connections at target companies on LinkedIn
- Offer value first: share their content, comment thoughtfully
- Then ask for a referral after building rapport

**{"Improve your ATS score first to increase interview callbacks!" if score < 60 else "Your profile looks strong — focus on networking and applying consistently!"}**"""

def _coach_salary(career_goal: str, skills: List[str]) -> str:
    goal = career_goal or "Software Engineer"
    
    return f"""Here's salary negotiation guidance for **{goal}** roles:

**Market Research:**
- Use Levels.fyi, Glassdoor, LinkedIn Salary, and Payscale
- Search by role + location + years of experience
- Target the 75th percentile, not the median

**Negotiation Strategy:**
1. Never give a number first — "I'd like to understand the full package"
2. When asked, give a range: "Based on my research and experience, I'm targeting $X-$Y"
3. Always negotiate — 85% of offers have flexibility
4. Consider total comp: base + bonus + equity + benefits

**Skills that increase salary for {goal}:**
{chr(10).join(f"- {s}" for s in (skills[:4] if skills else ["Cloud platforms", "System design", "Leadership", "Specialized domain expertise"]))}

**Counter-offer Script:**
"Thank you for the offer. I'm very excited about this opportunity. Based on my research and the value I bring, especially [specific skill], I was expecting something closer to [X]. Is there flexibility?"

**Know Your Worth:**
If you have strong projects, certifications, and interview scores above 80%, negotiate confidently for the higher end of market rates."""

def _coach_networking(career_goal: str) -> str:
    return f"""Networking strategy for breaking into **{career_goal or 'tech'}**:

**LinkedIn Optimization (Do this first):**
1. Professional photo (3x more profile views)
2. Compelling headline: "Aspiring {career_goal} | Python | FastAPI | Building AI Tools"
3. Summary: Your story, skills, and what you're looking for
4. Add all projects, certifications, and skills

**Networking Approach:**
1. **Connect with purpose** — target 5 people/week at companies you want to join
2. **Engage before connecting** — comment on their posts first
3. **Value-first message:** "I saw your post about X, I'm learning X and found Y helpful. Would love to connect!"
4. **Coffee chat request** — "I'm exploring careers in [field]. Would you spare 20 minutes for a virtual coffee chat?"

**Communities to join:**
- Discord: AI/ML communities, dev.to, Hashnode
- Reddit: r/cscareerquestions, r/MachineLearning, r/webdev
- Twitter/X: Follow thought leaders in your space
- Meetup.com: Local tech meetups

**The 80/20 Rule:** 80% of jobs are filled through networking. Build relationships before you need them."""

def _coach_default(career_goal: str, ats_score: float, roadmap_progress: float, interview_stats: Dict, skills: List[str]) -> str:
    goal = career_goal or "your career goal"
    return f"""Hello! I'm your AI Career Coach. Here's a snapshot of where you stand:

**Your Career Dashboard:**
- 🎯 Career Goal: {goal}
- 📄 ATS Score: {ats_score:.0f}%
- 🗺️ Roadmap Progress: {roadmap_progress:.0f}%
- 🎤 Interviews Completed: {interview_stats.get("total_completed", 0)}
- ⭐ Avg Interview Score: {interview_stats.get("avg_score", 0):.0f}%

**I can help you with:**
1. 📚 "What should I learn next?" — personalized study plan
2. 📄 "How can I improve my ATS score?" — resume optimization tips
3. 💻 "Which projects should I build?" — portfolio recommendations
4. 🏆 "Which certifications are valuable?" — cert roadmap
5. 🎤 "How can I prepare for interviews?" — interview strategy
6. 💼 "Recommend jobs based on my skills" — job search guidance
7. 💰 "How do I negotiate my salary?" — negotiation tactics

**Quick Recommendation:**
{"Your ATS score needs attention — improving your resume keywords could 2x your callback rate. Ask me: 'How can I improve my ATS score?'" if ats_score < 60 else "Your profile looks solid! Focus on interview prep to convert more applications into offers. Ask me: 'How can I prepare for interviews?'"}

What would you like to work on today?"""
