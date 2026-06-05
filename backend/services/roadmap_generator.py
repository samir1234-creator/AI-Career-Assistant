import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from domain.schemas.roadmap_schema import (
    RoadmapResponse, RoadmapMonthlyPlan, RoadmapWeeklyPlan,
    RoadmapResourceItem, RoadmapProjectItem, MilestoneProgressTracker,
    RoadmapProgressInfo, JobMarketIntelligence, CareerOutcomeForecast
)
from services.milestone_engine import MilestoneProgressEngine
from services.duration_engine import DurationEngine
from services.career_scoring_engine import CareerScoringEngine
from services.intelligent_syllabus import IntelligentSyllabusGenerator

logger = logging.getLogger(__name__)

# Career-specific eligible roles mapping for outcome forecasting
ELIGIBLE_ROLES_MAP: Dict[str, List[str]] = {
    "AI Engineer": ["AI Engineer", "Machine Learning Engineer", "NLP Engineer", "Generative AI Engineer", "LLM Engineer"],
    "Machine Learning Engineer": ["Machine Learning Engineer", "AI Engineer", "Data Scientist", "MLOps Engineer"],
    "Data Scientist": ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "Research Scientist"],
    "Data Analyst": ["Data Analyst", "Business Intelligence Analyst", "Data Scientist (Junior)", "Analytics Engineer"],
    "Full Stack Developer": ["Full Stack Developer", "Frontend Developer", "Backend Developer", "Software Engineer"],
    "Software Engineer": ["Software Engineer", "Backend Developer", "Full Stack Developer", "Systems Engineer"],
    "DevOps Engineer": ["DevOps Engineer", "Site Reliability Engineer", "Platform Engineer", "Cloud Engineer"],
    "Cloud Engineer": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect", "Infrastructure Engineer"],
    "Cybersecurity Engineer": ["Cybersecurity Engineer", "Penetration Tester", "Security Analyst", "SOC Analyst"],
    "Blockchain Developer": ["Blockchain Developer", "Smart Contract Engineer", "Web3 Developer", "DeFi Engineer"],
    "Mobile Developer": ["Mobile Developer", "iOS Developer", "Android Developer", "React Native Developer"],
    "UI/UX Designer": ["UI/UX Designer", "Product Designer", "Interaction Designer", "Design Systems Engineer"],
    "Product Manager": ["Product Manager", "Senior Product Manager", "Group Product Manager", "Director of Product"],
}

# Default badge/achievement groups per career
CAREER_BADGE_GROUPS: Dict[str, List[Dict[str, Any]]] = {
    "AI Engineer": [
        {"id": "ml_explorer", "name": "Machine Learning Explorer", "emoji": "🤖", "milestone_indices": [1]},
        {"id": "dl_specialist", "name": "Deep Learning Specialist", "emoji": "🧠", "milestone_indices": [2, 3]},
        {"id": "nlp_practitioner", "name": "NLP Practitioner", "emoji": "📝", "milestone_indices": [4]},
        {"id": "llm_builder", "name": "LLM Builder", "emoji": "💡", "milestone_indices": [5]},
        {"id": "genai_engineer", "name": "Generative AI Engineer", "emoji": "✨", "milestone_indices": [6, 7]},
        {"id": "cloud_practitioner", "name": "Cloud Practitioner", "emoji": "☁️", "milestone_indices": [8]},
        {"id": "career_ready", "name": "AI Career Ready", "emoji": "🚀", "milestone_indices": []},  # auto-unlocks on 100%
    ],
}


class RoadmapGenerator:
    def __init__(self, core_dir: Optional[str] = None):
        current_dir = Path(__file__).resolve().parent
        if core_dir is None:
            core_dir = str(current_dir.parent / "core")

        self.core_dir = Path(core_dir)
        self.templates_path = self.core_dir / "roadmap_templates.json"
        self.resources_path = self.core_dir / "learning_resources.json"
        self.projects_path = self.core_dir / "project_recommendations.json"
        self.dependencies_path = self.core_dir / "skill_dependency_database.json"
        self.job_market_path = self.core_dir / "job_market_intelligence.json"

        self.templates: Dict[str, Any] = {}
        self.resources: Dict[str, List[Dict[str, str]]] = {}
        self.projects: Dict[str, List[Dict[str, str]]] = {}
        self.job_market_db: Dict[str, Any] = {}

        self.milestone_engine = MilestoneProgressEngine(
            templates_path=str(self.core_dir / "milestone_templates.json"),
            dependency_path=str(self.dependencies_path)
        )

        self._load_databases()

    def _load_databases(self) -> None:
        try:
            if self.templates_path.exists():
                with open(self.templates_path, "r", encoding="utf-8") as f:
                    self.templates = json.load(f)

            if self.resources_path.exists():
                with open(self.resources_path, "r", encoding="utf-8") as f:
                    self.resources = json.load(f)

            if self.projects_path.exists():
                with open(self.projects_path, "r", encoding="utf-8") as f:
                    self.projects = json.load(f)

            if self.job_market_path.exists():
                with open(self.job_market_path, "r", encoding="utf-8") as f:
                    self.job_market_db = json.load(f)

        except Exception as e:
            logger.error(f"Failed to load roadmap database files: {str(e)}")

    def _get_skill_resources(self, skill: str) -> List[RoadmapResourceItem]:
        """Return curated resources for a skill (up to 8 items)."""
        skill_lower = skill.lower().strip()
        skill_resources = []
        if skill_lower in self.resources:
            for res in self.resources[skill_lower][:8]:
                skill_resources.append(RoadmapResourceItem(
                    name=res["name"],
                    url=res["url"],
                    type=res.get("type", "Course")
                ))
        return skill_resources

    def _get_skill_projects(self, skill: str) -> List[RoadmapProjectItem]:
        """Return portfolio projects for a skill (Beginner + Intermediate + Advanced)."""
        skill_lower = skill.lower().strip()
        result = []
        if skill_lower in self.projects:
            for proj in self.projects[skill_lower]:
                result.append(RoadmapProjectItem(
                    title=proj["title"],
                    description=proj["description"],
                    difficulty=proj.get("difficulty", "Intermediate"),
                    tech=proj.get("tech", []),
                    estimated_hours=proj.get("estimated_hours")
                ))
        return result

    def _get_skill_learning_time(self, skill: str, matched_skills: List[str]) -> int:
        """Personalized timeline estimation delegating to DurationEngine."""
        return DurationEngine.get_skill_duration_weeks(
            skill=skill,
            matched_skills=matched_skills,
            dependency_db=self.milestone_engine.dependency_db
        )

    def _build_job_market(self, career: str) -> Optional[JobMarketIntelligence]:
        """Load job market intelligence for the given career."""
        data = self.job_market_db.get(career)
        if not data:
            return None
        try:
            return JobMarketIntelligence(
                india_salary=data.get("india_salary", {}),
                global_salary=data.get("global_salary", {}),
                demand_level=data.get("demand_level", "High"),
                hiring_trend=data.get("hiring_trend", "Steady"),
                trend_direction=data.get("trend_direction", "stable"),
                estimated_job_openings=data.get("estimated_job_openings", 0),
                yoy_growth=data.get("yoy_growth", "+0%"),
                top_employers=data.get("top_employers", []),
                remote_friendly=data.get("remote_friendly", True),
                certification_boost=data.get("certification_boost", [])
            )
        except Exception as e:
            logger.warning(f"Failed to build job market for {career}: {e}")
            return None

    def _generate_weekly_plan_details(self, skill: str, week_num: int, topics: List[str]) -> Tuple[List[str], List[str], str, str]:
        """Generate structured details for the weekly syllabus."""
        practice_tasks = [
            f"Set up and configure the local development environment for {skill}.",
            f"Build a small prototype implementing: {', '.join(topics[:2])}."
        ]
        mini_assignments = [
            f"Create a GitHub repository and commit a project utilizing {skill}.",
            f"Write a short technical documentation explaining the core components of {skill} studied this week."
        ]
        quiz = "10 Questions"
        expected_outcome = f"Master the foundational concepts of {skill} and demonstrate practical implementation of {', '.join(topics[:2])}."
        
        s_lower = skill.lower().strip()
        if "python" in s_lower:
            practice_tasks = [
                "Write Python scripts using advanced collections (lists, dicts, sets, tuples).",
                "Debug complex code involving custom exceptions and try-except blocks."
            ]
            mini_assignments = [
                "Develop a CLI application to parse and process data from a CSV file.",
                "Implement a script that queries a public REST API and parses the response."
            ]
            expected_outcome = "Comfortably write, debug, and structure clean Python code using standard libraries."
        elif "machine learning" in s_lower or "scikit-learn" in s_lower:
            practice_tasks = [
                "Preprocess a messy dataset using pandas and handle missing values.",
                "Train a logistic regression and a random forest model on a sample dataset."
            ]
            mini_assignments = [
                "Build an end-to-end classification pipeline using scikit-learn's Pipeline class.",
                "Evaluate model performance using precision, recall, and ROC-AUC metrics."
            ]
            expected_outcome = "Understand the machine learning lifecycle and train baseline classification/regression models."
        elif "deep learning" in s_lower or "pytorch" in s_lower or "tensorflow" in s_lower:
            practice_tasks = [
                "Build a simple feedforward neural network in PyTorch/TensorFlow.",
                "Implement backpropagation manually or trace gradient changes."
            ]
            mini_assignments = [
                "Train a convolutional neural network (CNN) on the CIFAR-10 image dataset.",
                "Use learning rate schedulers and early stopping to prevent model overfitting."
            ]
            expected_outcome = "Build, train, and hyperparameter-tune neural network models for image or sequence datasets."
        elif "llm" in s_lower or "generative ai" in s_lower or "langchain" in s_lower or "llamaindex" in s_lower or "rag" in s_lower:
            practice_tasks = [
                "Connect to the OpenAI or open-source model API and configure system prompts.",
                "Create a vector store index using local documents and query it."
            ]
            mini_assignments = [
                "Build a Retrieval-Augmented Generation (RAG) chatbot using LangChain or LlamaIndex.",
                "Implement conversation memory and trace query flows using LangSmith."
            ]
            expected_outcome = "Design and deploy agentic RAG systems leveraging vector databases and custom tool bindings."
        elif "aws" in s_lower or "cloud" in s_lower:
            practice_tasks = [
                "Create an AWS account and set up IAM users and permission groups.",
                "Launch an EC2 instance and connect to it via SSH."
            ]
            mini_assignments = [
                "Configure an S3 bucket with secure public/private access policies.",
                "Build a serverless REST API using AWS Lambda, API Gateway, and DynamoDB."
            ]
            expected_outcome = "Understand AWS Core Services, global infrastructure, and security shared responsibility models."
            
        return practice_tasks, mini_assignments, quiz, expected_outcome

    def _build_career_forecast(
        self, career: str, career_readiness: int,
        matched_skills: List[str], missing_skills: List[str],
        total_weeks: int, projects: List[str], certifications: List[str],
        education: List[str], ats_score: int
    ) -> CareerOutcomeForecast:
        """Compute career outcome forecast metrics using CareerScoringEngine."""
        demand = "High"
        data = self.job_market_db.get(career)
        if data:
            demand = data.get("demand_level", "High")
            
        scores = CareerScoringEngine.calculate_scores(
            career_name=career,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            projects=projects,
            certifications=certifications,
            education=education,
            ats_score=ats_score,
            demand_level=demand
        )
        
        current = scores["current_readiness"]
        projected = scores["projected_readiness"]
        success_prob = scores["success_probability"]
        
        eligible = ELIGIBLE_ROLES_MAP.get(career, [career])
        
        months = total_weeks / 4.0
        if months <= 1:
            time_str = f"{total_weeks} week{'s' if total_weeks != 1 else ''}"
        elif months < 1.5:
            time_str = "~1 month"
        else:
            time_str = f"~{round(months)} months"
            
        return CareerOutcomeForecast(
            current_readiness=current,
            projected_readiness=projected,
            success_probability=success_prob,
            eligible_roles=eligible,
            time_to_job_ready=time_str,
            skills_mastered=len(matched_skills),
            skills_remaining=len(missing_skills)
        )

    def generate(
        self, career: str, matched_skills: List[str],
        missing_skills: List[str], career_readiness: int,
        projects: Optional[List[str]] = None,
        certifications: Optional[List[str]] = None,
        education: Optional[List[str]] = None,
        ats_score: int = 70
    ) -> RoadmapResponse:
        """
        Generates a full dependency-aware career roadmap.
        """
        projects = projects or []
        certifications = certifications or []
        education = education or []

        # ---- Step 1: Centralized scoring engine score query ----
        demand = "High"
        job_market_data = self.job_market_db.get(career)
        if job_market_data:
            demand = job_market_data.get("demand_level", "High")
            
        scores = CareerScoringEngine.calculate_scores(
            career_name=career,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            projects=projects,
            certifications=certifications,
            education=education,
            ats_score=ats_score,
            demand_level=demand
        )
        
        # Sync scores with engine
        career_readiness = scores["current_readiness"]
        expected_readiness = scores["projected_readiness"]

        # ---- Step 2: Topological milestone generation ----
        raw_milestones = self.milestone_engine.generate_milestones(career, missing_skills)

        # Flatten sorted skills from milestones (exclude final "Ready" milestone)
        sorted_missing_skills = []
        for m in raw_milestones[:-1]:
            for s in m["skills"]:
                if s not in sorted_missing_skills:
                    sorted_missing_skills.append(s)

        # ---- Step 3: Build week-by-week timeline ----
        weekly_timeline = []
        absolute_week_idx = 1

        for skill in sorted_missing_skills:
            total_skill_weeks = self._get_skill_learning_time(skill, matched_skills)
            skill_resources = self._get_skill_resources(skill)

            for w in range(1, total_skill_weeks + 1):
                # Call the IntelligentSyllabusGenerator to get structured, progressive content
                week_details = IntelligentSyllabusGenerator.generate_week(skill, w, total_skill_weeks, templates=self.templates)

                weekly_timeline.append({
                    "week_number": absolute_week_idx,
                    "skill": skill,
                    "title": week_details["title"],
                    "description": week_details["description"],
                    "topics": week_details["topics"],
                    "resources": skill_resources,
                    "practice_tasks": week_details["practice_tasks"],
                    "mini_assignments": week_details["mini_assignments"],
                    "quiz": week_details["quiz"],
                    "expected_outcome": week_details["expected_outcome"],
                    "estimated_hours": week_details["estimated_hours"]
                })
                absolute_week_idx += 1

        # ---- Step 4: Partition into monthly plans ----
        monthly_plans = []
        total_learning_weeks = len(weekly_timeline)
        total_months = max(1, (total_learning_weeks + 3) // 4)

        for m in range(1, total_months + 1):
            start_idx = (m - 1) * 4
            end_idx = min(start_idx + 4, total_learning_weeks)
            month_weeks_data = weekly_timeline[start_idx:end_idx]

            month_skills = []
            for w_data in month_weeks_data:
                if w_data["skill"] not in month_skills:
                    month_skills.append(w_data["skill"])

            primary_skill = month_skills[0] if month_skills else "General Tech"
            # Pass total_months to build progressive stage titles (Beginner -> Intermediate -> Advanced -> Project)
            month_title = self._build_month_title(m, primary_skill, month_skills, total_months)
            goals = [w["title"] for w in month_weeks_data]

            # Projects per month (Beginner + Intermediate + Advanced from first skill)
            recommended_projects = []
            for s in month_skills:
                projs = self._get_skill_projects(s)
                recommended_projects.extend(projs)
                if len(recommended_projects) >= 3:
                    break

            if not recommended_projects:
                recommended_projects.append(RoadmapProjectItem(
                    title=f"Practical {primary_skill} Implementation",
                    description=f"Design, build and evaluate a module integrating {primary_skill} concepts learned this month.",
                    difficulty="Intermediate",
                    tech=[primary_skill]
                ))

            weeks = [
                RoadmapWeeklyPlan(
                    week_number=w["week_number"],
                    title=w["title"],
                    description=w["description"],
                    topics=w["topics"],
                    resources=w["resources"],
                    practice_tasks=w["practice_tasks"],
                    mini_assignments=w["mini_assignments"],
                    quiz=w["quiz"],
                    expected_outcome=w["expected_outcome"],
                    estimated_hours=w["estimated_hours"]
                ) for w in month_weeks_data
            ]

            monthly_plans.append(RoadmapMonthlyPlan(
                month_number=m,
                title=month_title,
                skills=month_skills,
                goals=goals[:4],
                weeks=weeks,
                projects=recommended_projects
            ))

        # ---- Step 5: Capstone portfolio month ----
        portfolio_month_num = total_months + 1
        portfolio_projects = []
        if "portfolio project" in self.projects:
            for proj in self.projects["portfolio project"]:
                portfolio_projects.append(RoadmapProjectItem(
                    title=proj["title"],
                    description=proj["description"],
                    difficulty=proj.get("difficulty", "Advanced"),
                    tech=proj.get("tech", [])
                ))
        else:
            portfolio_projects.append(RoadmapProjectItem(
                title=f"{career} Portfolio Project",
                description=f"Deploy a complete {career} application demonstrating all skills acquired during the roadmap.",
                difficulty="Advanced",
                tech=sorted_missing_skills[-3:] if len(sorted_missing_skills) >= 3 else sorted_missing_skills
            ))

        portfolio_weeks = []
        pf_tasks = [
            ("Project Scoping & Architecture Design", ["Drafting system architecture", "Selecting datasets / APIs", "Writing technical specification"]),
            ("Backend & Core Logic Development", ["Implementing services and logic", "Writing unit tests", "API integration"]),
            ("Frontend & Dashboard Integration", ["Designing UI components", "Connecting API responses", "Responsive layout implementation"]),
            ("Deployment & Portfolio Polish", ["Hosting publicly on cloud", "Writing README & documentation", "Performance optimization"])
        ]
        for w_idx, (task_title, task_topics) in enumerate(pf_tasks, start=1):
            practice = [
                f"Work on the core implementation of the Capstone project phase: {task_title}.",
                "Commit code changes to the repository and document architectural decisions."
            ]
            assignments = [
                f"Complete and verify the deliverables for {task_title} milestone."
            ]
            outcome = f"Successful completion of the capstone project phase: {task_title}."
            quiz = "No quiz (Milestone assignment evaluation)"
            desc = f"Execute deliverables for the Capstone Portfolio project phase: {task_title}."

            portfolio_weeks.append(RoadmapWeeklyPlan(
                week_number=total_learning_weeks + w_idx,
                title=task_title,
                description=desc,
                topics=task_topics,
                resources=[],
                practice_tasks=practice,
                mini_assignments=assignments,
                quiz=quiz,
                expected_outcome=outcome,
                estimated_hours=12
            ))

        monthly_plans.append(RoadmapMonthlyPlan(
            month_number=portfolio_month_num,
            title="Deployment: Capstone Portfolio Project",
            skills=[f"{career} Portfolio"],
            goals=["Design architecture", "Build backend services", "Build frontend UI", "Deploy publicly"],
            weeks=portfolio_weeks,
            projects=portfolio_projects
        ))

        # ---- Step 6: Full milestone list with resources + projects ----
        matched_set = {s.lower().strip() for s in matched_skills}
        all_skills = matched_skills + missing_skills
        raw_all_milestones = self.milestone_engine.generate_milestones(career, all_skills)

        milestones = []
        completed_milestone_titles = []
        remaining_milestone_titles = []

        for m in raw_all_milestones:
            m_idx = m["index"]
            m_title = m["title"]
            m_skills = m["skills"]

            is_final = "ready" in m_title.lower()
            if is_final:
                is_complete = len(missing_skills) == 0 or career_readiness >= 91
            else:
                is_complete = all(s.lower().strip() in matched_set for s in m_skills)

            m_resources = []
            m_projects = []
            for skill in m_skills:
                if not is_final:
                    m_resources.extend(self._get_skill_resources(skill))
                    m_projects.extend(self._get_skill_projects(skill))

            seen_urls = set()
            unique_resources = []
            for r in m_resources:
                if r.url not in seen_urls:
                    seen_urls.add(r.url)
                    unique_resources.append(r)

            milestones.append(MilestoneProgressTracker(
                index=m_idx,
                title=m_title,
                skills=m_skills,
                complete=is_complete,
                resources=unique_resources,
                projects=m_projects
            ))

            if is_complete:
                completed_milestone_titles.append(m_title)
            else:
                remaining_milestone_titles.append(m_title)

        # ---- Step 7: Progress info ----
        progress_info = RoadmapProgressInfo(
            completion_percentage=career_readiness,
            current_month=1,
            completed_milestones=completed_milestone_titles,
            remaining_milestones=remaining_milestone_titles
        )

        # ---- Step 8: Difficulty classification ----
        difficulty = "Intermediate"
        if len(missing_skills) > 6 or any(s.lower() in ["deep learning", "llms", "generative ai", "kubernetes"] for s in missing_skills):
            difficulty = "Advanced"
        elif len(missing_skills) <= 3:
            difficulty = "Beginner"

        # ---- Step 9: Job market intelligence ----
        job_market = self._build_job_market(career)

        # ---- Step 10: Dynamic Durations ----
        total_timeline_weeks = total_learning_weeks + len(portfolio_weeks)
        
        # Calculate synchronized completion values from DurationEngine
        duration_info = DurationEngine.calculate_total_duration(
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            dependency_db=self.milestone_engine.dependency_db
        )
        
        # Ensure values stay strictly in sync
        total_timeline_weeks = duration_info["total_weeks"]
        portfolio_month_num = duration_info["total_months"]

        career_forecast = self._build_career_forecast(
            career, career_readiness, matched_skills, missing_skills, 
            total_timeline_weeks, projects, certifications, education, ats_score
        )

        return RoadmapResponse(
            career=career,
            expected_readiness=expected_readiness,
            difficulty=difficulty,
            total_weeks=total_timeline_weeks,
            total_months=portfolio_month_num,
            monthly_roadmap=monthly_plans,
            milestones=milestones,
            progress=progress_info,
            job_market=job_market,
            career_forecast=career_forecast
        )

    def _build_month_title(self, month_num: int, primary_skill: str, month_skills: List[str], total_months: int) -> str:
        """Generate a descriptive month title based on primary skill and progression stage."""
        # Determine the progression stage prefix
        if month_num == 1:
            stage = "Beginner"
        elif month_num == total_months:
            stage = "Project"
        else:
            # Intermediate months between 1 and total_months
            midpoint = (1 + total_months) / 2
            if month_num < midpoint:
                stage = "Intermediate"
            else:
                stage = "Advanced"

        title_overrides = {
            "deep learning": "Deep Learning Fundamentals",
            "pytorch": "PyTorch Framework Mastery",
            "tensorflow": "TensorFlow & Keras Pipelines",
            "nlp": "Natural Language Processing",
            "llms": "Large Language Models (LLMs)",
            "generative ai": "Generative AI Architectures",
            "langchain": "LangChain & LlamaIndex Tools",
            "llamaindex": "LlamaIndex & RAG Systems",
            "mlops": "MLOps & Production Deployment",
            "docker": "Containerization with Docker",
            "kubernetes": "Kubernetes Orchestration",
            "aws": "AWS Cloud Services",
            "react": "React Frontend Development",
            "machine learning": "Machine Learning Core",
            "python": "Python Programming Mastery",
            "sql": "SQL & Database Fundamentals",
            "penetration testing": "Ethical Hacking & Pentesting",
            "solidity": "Smart Contract Development",
            "terraform": "Infrastructure as Code",
        }

        p_lower = primary_skill.lower().strip()
        if p_lower in title_overrides:
            base_title = title_overrides[p_lower]
        elif month_num == 1:
            base_title = f"{primary_skill} & Foundations"
        elif len(month_skills) > 1:
            base_title = f"{primary_skill} & {month_skills[1]}"
        else:
            base_title = f"{primary_skill} Mastery"

        return f"{stage}: {base_title}"
