import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

DEFAULT_SKILL_WEEKS = {
    "python": 4, "java": 6, "javascript": 4, "typescript": 4, "go": 4, "rust": 6,
    "c++": 8, "c#": 6, "machine learning": 6, "deep learning": 6, "nlp": 3,
    "llms": 5, "generative ai": 4, "langchain": 2, "llamaindex": 2, "pytorch": 3,
    "tensorflow": 4, "docker": 2, "kubernetes": 4, "aws": 4, "sql": 3,
    "databases": 3, "html5": 1, "css3": 2, "react": 4, "node.js": 4, "git": 1,
    "mlops": 4, "linux": 2, "networking": 3, "cloud computing": 3,
    "penetration testing": 5, "solidity": 4, "blockchain fundamentals": 3,
    "figma": 2, "ui/ux design": 3, "product management": 4, "agile": 2
}

_templates_cache = None

def _get_templates() -> Dict[str, Any]:
    global _templates_cache
    if _templates_cache is not None:
        return _templates_cache
    try:
        current_dir = Path(__file__).resolve().parent
        templates_path = current_dir.parent / "core" / "roadmap_templates.json"
        if templates_path.exists():
            with open(templates_path, "r", encoding="utf-8") as f:
                _templates_cache = json.load(f)
                return _templates_cache
    except Exception as e:
        logger.error(f"Failed to load roadmap templates in DurationEngine: {e}")
    _templates_cache = {}
    return _templates_cache

class DurationEngine:
    @staticmethod
    def get_skill_duration_weeks(
        skill: str,
        matched_skills: List[str],
        dependency_db: Dict[str, List[str]]
    ) -> int:
        """
        Calculate learning duration in weeks for a single skill.
        If the user knows a prerequisite, reduce the duration by 30%.
        """
        skill_lower = skill.lower().strip()
        templates = _get_templates()
        
        # 1. Template-based duration
        if skill_lower in templates:
            base_weeks = templates[skill_lower].get("default_weeks", 4)
        else:
            base_weeks = DEFAULT_SKILL_WEEKS.get(skill_lower, 3)

        # 2. Reduction if user knows any prerequisite
        matched_lower = {s.lower().strip() for s in matched_skills}
        prereqs = []
        for k, deps in dependency_db.items():
            if k.lower().strip() == skill_lower:
                prereqs = [d.lower().strip() for d in deps]
                break

        if any(p in matched_lower for p in prereqs):
            base_weeks = max(1, round(base_weeks * 0.7))

        return int(base_weeks)

    @staticmethod
    def calculate_total_duration(
        missing_skills: List[str],
        matched_skills: List[str],
        dependency_db: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Calculates total weeks, months, study hours, workloads, and estimated completion date.
        """
        # Sum of weeks for all missing skills
        learning_weeks = 0
        for skill in missing_skills:
            learning_weeks += DurationEngine.get_skill_duration_weeks(skill, matched_skills, dependency_db)

        # Add 4 weeks for Capstone Portfolio project
        total_weeks = learning_weeks + 4
        
        # Total months (assuming 4 weeks per month)
        total_months = max(1, (total_weeks + 3) // 4)
        
        # Workloads
        weekly_hours = "8 hours" # Standard weekly workload: 8 study hours/week
        monthly_hours = "32 hours" # Standard monthly workload: 32 study hours/month
        total_study_hours = total_weeks * 8
        
        # Estimated completion date from June 5, 2026
        base_date = datetime(2026, 6, 5)
        completion_date = base_date + timedelta(weeks=total_weeks)
        
        # Format date as e.g. "Feb 2027" or "February 2027"
        date_str = completion_date.strftime("%B %Y") # e.g. "February 2027"
        date_short = completion_date.strftime("%b %d, %Y") # e.g. "Feb 05, 2027"

        return {
            "total_weeks": total_weeks,
            "total_months": total_months,
            "total_study_hours": total_study_hours,
            "weekly_workload": weekly_hours,
            "monthly_workload": monthly_hours,
            "estimated_completion_date": date_short,
            "estimated_completion_month": date_str
        }
