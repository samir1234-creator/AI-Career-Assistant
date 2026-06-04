import json
import logging
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from domain.schemas.skill_gap_schema import (
    SkillGapRequest, SkillGapResponse, SkillGapItem, SkillGapInsights, RoadmapSkillItem, MilestoneItem
)
from services.skill_intelligence_service import SkillIntelligenceService
from services.milestone_engine import MilestoneProgressEngine

logger = logging.getLogger(__name__)

SKILL_METADATA_DEFAULTS = {
    "python": {"priority": "critical", "impact_score": 90, "estimated_learning_time": "4 weeks"},
    "java": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "6 weeks"},
    "javascript": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "4 weeks"},
    "typescript": {"priority": "important", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "go": {"priority": "important", "impact_score": 75, "estimated_learning_time": "4 weeks"},
    "golang": {"priority": "important", "impact_score": 75, "estimated_learning_time": "4 weeks"},
    "rust": {"priority": "important", "impact_score": 80, "estimated_learning_time": "6 weeks"},
    "c++": {"priority": "critical", "impact_score": 90, "estimated_learning_time": "8 weeks"},
    "c#": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "6 weeks"},
    
    "docker": {"priority": "important", "impact_score": 75, "estimated_learning_time": "2 weeks"},
    "kubernetes": {"priority": "important", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "aws": {"priority": "important", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "azure": {"priority": "important", "impact_score": 75, "estimated_learning_time": "4 weeks"},
    "gcp": {"priority": "important", "impact_score": 75, "estimated_learning_time": "4 weeks"},
    "cloud computing": {"priority": "important", "impact_score": 70, "estimated_learning_time": "3 weeks"},
    "terraform": {"priority": "important", "impact_score": 75, "estimated_learning_time": "3 weeks"},
    "ci/cd": {"priority": "important", "impact_score": 80, "estimated_learning_time": "2 weeks"},
    "jenkins": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    "linux": {"priority": "critical", "impact_score": 80, "estimated_learning_time": "3 weeks"},
    "git": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "1 week"},
    
    "sql": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "3 weeks"},
    "databases": {"priority": "critical", "impact_score": 80, "estimated_learning_time": "3 weeks"},
    "mongodb": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    "postgresql": {"priority": "important", "impact_score": 75, "estimated_learning_time": "2 weeks"},
    "mysql": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    "redis": {"priority": "optional", "impact_score": 50, "estimated_learning_time": "2 weeks"},
    "firebase": {"priority": "optional", "impact_score": 45, "estimated_learning_time": "2 weeks"},
    
    "react": {"priority": "critical", "impact_score": 90, "estimated_learning_time": "4 weeks"},
    "next.js": {"priority": "important", "impact_score": 80, "estimated_learning_time": "3 weeks"},
    "angular": {"priority": "important", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "vue.js": {"priority": "important", "impact_score": 75, "estimated_learning_time": "3 weeks"},
    "html5": {"priority": "critical", "impact_score": 80, "estimated_learning_time": "1 week"},
    "css3": {"priority": "critical", "impact_score": 80, "estimated_learning_time": "2 weeks"},
    "tailwind css": {"priority": "optional", "impact_score": 55, "estimated_learning_time": "1 week"},
    "redux": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    
    "node.js": {"priority": "critical", "impact_score": 90, "estimated_learning_time": "4 weeks"},
    "express.js": {"priority": "critical", "impact_score": 80, "estimated_learning_time": "2 weeks"},
    "fastapi": {"priority": "important", "impact_score": 75, "estimated_learning_time": "2 weeks"},
    "django": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "4 weeks"},
    "flask": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    "spring boot": {"priority": "critical", "impact_score": 90, "estimated_learning_time": "6 weeks"},
    "nestjs": {"priority": "important", "impact_score": 75, "estimated_learning_time": "3 weeks"},
    "rest apis": {"priority": "important", "impact_score": 80, "estimated_learning_time": "1 week"},
    
    "machine learning": {"priority": "critical", "impact_score": 95, "estimated_learning_time": "6 weeks"},
    "deep learning": {"priority": "critical", "impact_score": 95, "estimated_learning_time": "6 weeks"},
    "llms": {"priority": "critical", "impact_score": 90, "estimated_learning_time": "4-6 weeks"},
    "nlp": {"priority": "important", "impact_score": 75, "estimated_learning_time": "2-4 weeks"},
    "generative ai": {"priority": "important", "impact_score": 80, "estimated_learning_time": "2-4 weeks"},
    "langchain": {"priority": "optional", "impact_score": 40, "estimated_learning_time": "1-2 weeks"},
    "llamaindex": {"priority": "optional", "impact_score": 35, "estimated_learning_time": "2 weeks"},
    "pytorch": {"priority": "important", "impact_score": 85, "estimated_learning_time": "3 weeks"},
    "tensorflow": {"priority": "important", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "scikit-learn": {"priority": "important", "impact_score": 85, "estimated_learning_time": "2 weeks"},
    "data analysis": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "3 weeks"},
    "statistics": {"priority": "critical", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "tableau": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    "power bi": {"priority": "important", "impact_score": 70, "estimated_learning_time": "2 weeks"},
    "excel": {"priority": "important", "impact_score": 60, "estimated_learning_time": "1 week"},
    "mlops": {"priority": "important", "impact_score": 80, "estimated_learning_time": "4 weeks"},
    "vector databases": {"priority": "important", "impact_score": 75, "estimated_learning_time": "2 weeks"},
    "rag": {"priority": "important", "impact_score": 80, "estimated_learning_time": "2 weeks"},
    "prompt engineering": {"priority": "optional", "impact_score": 50, "estimated_learning_time": "1 week"},
    "fine-tuning": {"priority": "important", "impact_score": 75, "estimated_learning_time": "3 weeks"},
    
    "figma": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "2 weeks"},
    "project management": {"priority": "critical", "impact_score": 85, "estimated_learning_time": "4 weeks"},
    "agile": {"priority": "important", "impact_score": 70, "estimated_learning_time": "1 week"},
    "scrum": {"priority": "important", "impact_score": 70, "estimated_learning_time": "1 week"},
    "jira": {"priority": "important", "impact_score": 60, "estimated_learning_time": "1 week"}
}

class SkillGapAnalysisService:
    def __init__(self, db_path: Optional[str] = None, dep_path: Optional[str] = None):
        """
        Initializes the Skill Gap Analysis Service and loads career & dependency databases.
        """
        current_dir = Path(__file__).resolve().parent
        if db_path is None:
            db_path = str(current_dir.parent / "core" / "career_database.json")
        if dep_path is None:
            dep_path = str(current_dir.parent / "core" / "skill_dependency_database.json")
            
        self.db_path = db_path
        self.dep_path = dep_path
        
        self.career_db: Dict[str, Dict[str, Any]] = {}
        self.dependency_db: Dict[str, List[str]] = {}
        
        self._load_databases()
        self.skill_intel_service = SkillIntelligenceService()
        
        # Determine templates path
        templates_path = None
        if db_path:
            templates_path = str(Path(db_path).parent / "milestone_templates.json")
        self.milestone_engine = MilestoneProgressEngine(
            templates_path=templates_path,
            dependency_path=dep_path
        )

    def _load_databases(self) -> None:
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.career_db = {item["career_name"]: item for item in data}
                    else:
                        self.career_db = data
            
            if os.path.exists(self.dep_path):
                with open(self.dep_path, "r", encoding="utf-8") as f:
                    self.dependency_db = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load service databases: {str(e)}")

    def _parse_weeks_range(self, time_str: str) -> Tuple[float, float]:
        if not time_str:
            return 0.0, 0.0
        time_str = time_str.lower().strip()
        is_months = "month" in time_str
        
        range_match = re.search(r'(\d+)\s*[-to]+\s*(\d+)', time_str)
        if range_match:
            val_min = float(range_match.group(1))
            val_max = float(range_match.group(2))
        else:
            single_match = re.search(r'(\d+)', time_str)
            if single_match:
                val_min = float(single_match.group(1))
                val_max = val_min
            else:
                return 0.0, 0.0
                
        if is_months:
            val_min *= 4.0
            val_max *= 4.0
            
        return val_min, val_max

    def _get_effort_score(self, max_weeks: float, priority: str, skill_name: str) -> str:
        s_lower = skill_name.lower().strip()
        if "llm" in s_lower:
            return "Very High"
        if "deep learning" in s_lower:
            return "High"
        if "langchain" in s_lower or "llamaindex" in s_lower:
            return "Low"
            
        if max_weeks <= 2:
            return "Low"
        elif max_weeks <= 4:
            return "Medium"
        elif max_weeks <= 6:
            return "High"
        else:
            return "Very High"

    def _generate_priority_ranking(self, missing_items: List[Dict[str, Any]]) -> List[str]:
        items_by_name = {item["skill"].lower().strip(): item for item in missing_items}
        
        graph = {}
        in_degree = {}
        for skill_lower, item in items_by_name.items():
            raw_deps = []
            for dep_k, dep_list in self.dependency_db.items():
                if dep_k.lower().strip() == skill_lower:
                    raw_deps = dep_list
                    break
                    
            missing_deps = []
            for d in raw_deps:
                d_lower = d.lower().strip()
                if d_lower in items_by_name:
                    missing_deps.append(d_lower)
            
            graph[skill_lower] = missing_deps
            in_degree[skill_lower] = len(missing_deps)

        ordered_skills = []
        visited = set()
        
        def get_priority_val(item):
            p = item["priority"].lower()
            if p == "critical":
                p_val = 3
            elif p == "important":
                p_val = 2
            else:
                p_val = 1
            return p_val, item["impact_score"]

        while len(ordered_skills) < len(missing_items):
            available = [name for name, deg in in_degree.items() if deg == 0 and name not in visited]
            
            if not available:
                unvisited = [name for name in items_by_name if name not in visited]
                if not unvisited:
                    break
                unvisited.sort(key=lambda name: get_priority_val(items_by_name[name]), reverse=True)
                candidate = unvisited[0]
                in_degree[candidate] = 0
                available = [candidate]

            available.sort(key=lambda name: get_priority_val(items_by_name[name]), reverse=True)
            
            next_node = available[0]
            visited.add(next_node)
            ordered_skills.append(items_by_name[next_node]["skill"])
            
            for name, deps in graph.items():
                if next_node in deps:
                    deps.remove(next_node)
                    in_degree[name] = len(deps)
                    
        return ordered_skills

    def analyze_gap(self, payload: SkillGapRequest) -> SkillGapResponse:
        career_name = payload.career
        matched_skills = payload.matched_skills
        missing_skills = payload.missing_skills

        # Find target career
        career_entry = None
        for name, entry in self.career_db.items():
            if name.lower().strip() == career_name.lower().strip():
                career_entry = entry
                break

        db_skills_meta = {}
        if career_entry and "skills_metadata" in career_entry:
            for item in career_entry["skills_metadata"]:
                db_skills_meta[item["skill"].lower().strip()] = item

        critical_skills = []
        important_skills = []
        optional_skills = []
        roadmap_compatibility = []
        missing_categories = {}

        total_penalty = 0.0
        job_ready_min_weeks = 0.0
        job_ready_max_weeks = 0.0

        raw_missing_list = []

        for skill in missing_skills:
            skill_lower = skill.lower().strip()
            priority = None
            impact_score = None
            learning_time = None

            # 1. Lookup in career metadata
            if skill_lower in db_skills_meta:
                meta = db_skills_meta[skill_lower]
                priority = meta.get("priority")
                impact_score = meta.get("impact_score")
                learning_time = meta.get("estimated_learning_time")

            # 2. Lookup in defaults
            default_meta = SKILL_METADATA_DEFAULTS.get(skill_lower)
            if default_meta:
                priority = priority or default_meta.get("priority")
                impact_score = impact_score or default_meta.get("impact_score")
                learning_time = learning_time or default_meta.get("estimated_learning_time")

            # 3. Fallback based on career lists
            if career_entry:
                req_list_lower = [s.lower().strip() for s in career_entry.get("required_skills", [])]
                pref_list_lower = [s.lower().strip() for s in career_entry.get("preferred_skills", [])]
                
                if skill_lower in req_list_lower:
                    priority = priority or "critical"
                    impact_score = impact_score or 85
                    learning_time = learning_time or "4 weeks"
                elif skill_lower in pref_list_lower:
                    priority = priority or "optional"
                    impact_score = impact_score or 45
                    learning_time = learning_time or "2 weeks"

            # 4. Ultimate defaults
            priority = (priority or "optional").strip().title()
            impact_score = impact_score or 30
            learning_time = learning_time or "2 weeks"

            if priority.lower() == "critical":
                priority_clean = "Critical"
                penalty_weight = 0.095
            elif priority.lower() == "important":
                priority_clean = "Important"
                penalty_weight = 0.065
            else:
                priority_clean = "Optional"
                penalty_weight = 0.02

            total_penalty += impact_score * penalty_weight

            # Parse learning time range
            min_w, max_w = self._parse_weeks_range(learning_time)
            
            # Accumulate time for critical/important skills
            if priority_clean in ["Critical", "Important"]:
                job_ready_min_weeks += min_w
                job_ready_max_weeks += max_w

            effort_score = self._get_effort_score(max_w, priority_clean, skill)

            gap_item = SkillGapItem(
                skill=skill,
                priority=priority_clean,
                impact_score=impact_score,
                estimated_learning_time=learning_time,
                effort_score=effort_score
            )

            raw_missing_list.append({
                "skill": skill,
                "priority": priority_clean,
                "impact_score": impact_score,
                "learning_time_weeks": int(round(max_w))
            })

            if priority_clean == "Critical":
                critical_skills.append(gap_item)
            elif priority_clean == "Important":
                important_skills.append(gap_item)
            else:
                optional_skills.append(gap_item)

            # Group missing skills into categories
            category, _ = self.skill_intel_service.lookup_skill(skill)
            display_cat = category
            if category in ["Artificial Intelligence", "Machine Learning", "Deep Learning", "Generative AI"]:
                display_cat = "AI Skills"
            elif category in ["Frontend Frameworks", "Backend Frameworks", "Frontend Framework", "Backend Framework"]:
                display_cat = "Frameworks"
            elif category in ["Cloud Computing", "Cloud"]:
                display_cat = "Cloud"
            elif category in ["Tools & Technologies", "Tools"]:
                display_cat = "Tools"
            
            if display_cat not in missing_categories:
                missing_categories[display_cat] = []
            missing_categories[display_cat].append(skill)

            # Roadmap Compatibility item
            raw_deps = []
            for dep_k, dep_list in self.dependency_db.items():
                if dep_k.lower().strip() == skill_lower:
                    raw_deps = dep_list
                    break
            
            roadmap_compatibility.append(RoadmapSkillItem(
                skill=skill,
                priority=priority_clean.lower(),
                impact_score=impact_score,
                learning_time_weeks=int(round(max_w)),
                dependencies=raw_deps
            ))

        # Sort lists by impact score descending
        critical_skills.sort(key=lambda x: -x.impact_score)
        important_skills.sort(key=lambda x: -x.impact_score)
        optional_skills.sort(key=lambda x: -x.impact_score)

        # Career Readiness Score
        readiness_score = int(round(100.0 - total_penalty))
        readiness_score = max(0, min(100, readiness_score))

        # Career Readiness Severity mapping
        if readiness_score >= 91:
            gap_severity = "Low Gap"
            readiness_level = "Job Ready"
        elif readiness_score >= 76:
            gap_severity = "Low Gap"
            readiness_level = "Nearly Job Ready"
        elif readiness_score >= 51:
            gap_severity = "Medium Gap"
            readiness_level = "Developing"
        elif readiness_score >= 26:
            gap_severity = "Medium Gap"
            readiness_level = "Early Stage"
        else:
            gap_severity = "High Gap"
            readiness_level = "Beginner"

        # Job Ready Ranges Formatting (Weeks and Months)
        min_w_int = int(round(job_ready_min_weeks))
        max_w_int = int(round(job_ready_max_weeks))
        if min_w_int == max_w_int:
            job_ready_time_weeks = f"{min_w_int} Week" if min_w_int == 1 else f"{min_w_int} Weeks"
        else:
            job_ready_time_weeks = f"{min_w_int}-{max_w_int} Weeks"

        min_m_int = int(round(job_ready_min_weeks / 4.0))
        max_m_int = int(round(job_ready_max_weeks / 4.0))
        if min_w_int > 0 and min_m_int == 0:
            min_m_int = 1
        if max_w_int > 0 and max_m_int == 0:
            max_m_int = 1

        if min_m_int == max_m_int:
            job_ready_time_months = f"{min_m_int} Month" if min_m_int == 1 else f"{min_m_int} Months"
        else:
            job_ready_time_months = f"{min_m_int}-{max_m_int} Months"

        # Exact learning priority ranking (topological sort)
        priority_ranking = self._generate_priority_ranking(raw_missing_list)

        # Insights summary text
        strong_bullets = "\n".join([f"✓ {s}" for s in matched_skills[:3]])
        if not strong_bullets:
            strong_bullets = "✓ None identified yet"
            
        prioritized_skills = []
        for item in critical_skills + important_skills:
            if len(prioritized_skills) < 3:
                prioritized_skills.append(item.skill)
        prioritize_bullets = "\n".join([f"✓ {s}" for s in prioritized_skills])
        if not prioritize_bullets:
            prioritize_bullets = "✓ No critical gaps identified"
        
        summary_text = (
            f"You already possess strong foundations in:\n{strong_bullets}\n\n"
            f"To become competitive for {career_name} roles, prioritize:\n{prioritize_bullets}"
        )

        insights = SkillGapInsights(
            strong_areas=matched_skills,
            weak_areas=[item.skill for item in critical_skills + important_skills],
            summary_text=summary_text
        )

        # Generate Milestones
        raw_milestones = self.milestone_engine.generate_milestones(career_name, missing_skills)
        milestones = [
            MilestoneItem(index=m["index"], title=m["title"], skills=m["skills"])
            for m in raw_milestones
        ]

        return SkillGapResponse(
            career=career_name,
            career_readiness=readiness_score,
            career_readiness_level=readiness_level,
            gap_severity=gap_severity,
            critical_skills=critical_skills,
            important_skills=important_skills,
            optional_skills=optional_skills,
            insights=insights,
            job_ready_time_weeks=job_ready_time_weeks,
            job_ready_time_months=job_ready_time_months,
            priority_ranking=priority_ranking,
            missing_categories=missing_categories,
            roadmap_compatibility=roadmap_compatibility,
            milestones=milestones
        )
