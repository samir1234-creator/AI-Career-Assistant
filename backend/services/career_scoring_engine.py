import json
import logging
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

_career_db_cache = None

def _load_career_db() -> Dict[str, Any]:
    global _career_db_cache
    if _career_db_cache is not None:
        return _career_db_cache
    try:
        current_dir = Path(__file__).resolve().parent
        db_path = current_dir.parent / "core" / "career_database.json"
        if db_path.exists():
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    _career_db_cache = {item["career_name"].lower().strip(): item for item in data}
                else:
                    _career_db_cache = {k.lower().strip(): v for k, v in data.items()}
                return _career_db_cache
    except Exception as e:
        logger.error(f"Failed to load career db in CareerScoringEngine: {e}")
    _career_db_cache = {}
    return _career_db_cache

class CareerScoringEngine:
    @staticmethod
    def _is_match(sub: str, parent: str) -> bool:
        db_s = sub.strip().lower()
        cand_s = parent.strip().lower()
        if db_s == cand_s:
            return True
        start = 0
        while True:
            idx = cand_s.find(db_s, start)
            if idx == -1:
                return False
            boundary_before = True
            if idx > 0:
                char_before = cand_s[idx - 1]
                if char_before.isalnum() or char_before in "+#.-":
                    boundary_before = False
            boundary_after = True
            end_idx = idx + len(db_s)
            if end_idx < len(cand_s):
                char_after = cand_s[end_idx]
                if char_after.isalnum() or char_after in "+#.-":
                    boundary_after = False
            if boundary_before and boundary_after:
                return True
            start = idx + 1

    @staticmethod
    def _get_derived_keywords(role: str, category: str) -> List[str]:
        keywords = [role.lower(), category.lower()]
        generic_words = {
            "engineer", "engineering", "developer", "development", "programmer", "coder", 
            "analyst", "analysis", "analytics", "architect", "architecture", "specialist", 
            "specialty", "manager", "management", "owner", "lead", "director", "consultant", 
            "administrator", "administration", "support", "designer", "design", "writer", 
            "writing", "expert", "officer", "app", "application", "software", "system", 
            "systems", "solutions", "associate", "assistant", "technician", "technology", 
            "technologies", "services", "service", "and", "for", "the", "with"
        }
        for word in re.findall(r'\b\w+\b', role.lower() + " " + category.lower()):
            if len(word) >= 2 and word not in generic_words:
                keywords.append(word)
        return list(set(keywords))

    @staticmethod
    def calculate_scores(
        career_name: str,
        matched_skills: List[str],
        missing_skills: List[str],
        projects: List[str],
        certifications: List[str],
        education: List[str],
        ats_score: int,
        demand_level: str = "High"
    ) -> Dict[str, Any]:
        """
        Unified Career Intelligence Scoring Engine.
        Returns synchronized percentages for:
        - Current Readiness
        - Projected Readiness
        - Success Probability
        """
        career_db = _load_career_db()
        career_key = career_name.lower().strip()
        career_entry = career_db.get(career_key)
        
        required_skills = []
        preferred_skills = []
        role_category = ""
        required_keywords = []
        if career_entry:
            required_skills = career_entry.get("required_skills", [])
            preferred_skills = career_entry.get("preferred_skills", [])
            role_category = career_entry.get("category", "")
            required_keywords = career_entry.get("required_keywords", [])
            if not demand_level or demand_level == "High":
                demand_level = career_entry.get("future_demand", demand_level)
                
        matched_lower = {s.lower().strip() for s in matched_skills}
        
        # Additive Skill Match calculation
        matched_req = [s for s in required_skills if s.lower().strip() in matched_lower]
        matched_pref = [s for s in preferred_skills if s.lower().strip() in matched_lower]
        
        req_score = min(len(matched_req) * 10.0, 28.0)
        pref_score = min(len(matched_pref) * 6.0, 12.0)
        skills_score = req_score + pref_score # Max 40.0
        
        project_count = len(projects)
        cert_count = len(certifications)
        
        is_pure_gap = (project_count == 0 and cert_count == 0 and len(education) == 0)
        
        if is_pure_gap:
            # Scale to 90 (at 32/40 it gives 72%)
            current_readiness = (skills_score / 40.0) * 90.0
        else:
            # Career-specific project/certification matching
            generic_skills_lower = {"python", "java", "c++", "c#", "sql", "git", "docker", "kubernetes", "linux", "html5", "css3", "javascript", "typescript", "it", "excel"}
            non_generic_req_skills = [s for s in required_skills if s.lower() not in generic_skills_lower]
            non_generic_pref_skills = [s for s in preferred_skills if s.lower() not in generic_skills_lower]
            derived_keywords = CareerScoringEngine._get_derived_keywords(career_name, role_category)
            
            project_score = 0.0
            has_relevant_project = False
            for p_desc in projects:
                if CareerScoringEngine._is_match(career_name, p_desc) or CareerScoringEngine._is_match(role_category, p_desc):
                    project_score = 20.0
                    has_relevant_project = True
                    break
            if not has_relevant_project:
                for p_desc in projects:
                    if any(CareerScoringEngine._is_match(kw, p_desc) for kw in derived_keywords + required_keywords + non_generic_req_skills + non_generic_pref_skills):
                        project_score = 15.0
                        has_relevant_project = True
                        break
                        
            cert_score = 0.0
            has_relevant_cert = False
            for cert_desc in certifications:
                if CareerScoringEngine._is_match(career_name, cert_desc) or CareerScoringEngine._is_match(role_category, cert_desc):
                    cert_score = 10.0
                    has_relevant_cert = True
                    break
            if not has_relevant_cert:
                for cert_desc in certifications:
                    if any(CareerScoringEngine._is_match(kw, cert_desc) for kw in derived_keywords + required_keywords + non_generic_req_skills + non_generic_pref_skills):
                        cert_score = 8.0
                        has_relevant_cert = True
                        break
                        
            ats_bonus = (ats_score / 100.0) * 10.0
            
            edu_bonus = 0.0
            if education:
                combined_edu = " ".join(education).lower()
                stem_keywords = ["computer science", "software", "engineering", "information technology", "mathematics", "statistics", "it"]
                if any(kw in combined_edu for kw in stem_keywords):
                    edu_bonus = 10.0
                else:
                    edu_bonus = 7.0
                    
            demand_bonus = 7.0
            if demand_level.lower() == "high":
                demand_bonus = 10.0
            elif demand_level.lower() == "low":
                demand_bonus = 4.0
                
            tie_breaker = 0.0
            if required_skills:
                tie_breaker = (len(matched_req) / len(required_skills)) * 2.0
                
            current_readiness = skills_score + project_score + cert_score + ats_bonus + edu_bonus + demand_bonus + tie_breaker
            
            # Disqualify if no required and preferred skills match and no projects/certs match
            if len(matched_skills) == 0 and project_count == 0 and cert_count == 0:
                current_readiness = 0.0

        # Round and Cap Current Readiness
        if not missing_skills:
            current_readiness = 100
        else:
            current_readiness = min(88, max(5, int(round(current_readiness))))

        # Calculate Projected Readiness
        if not missing_skills:
            roadmap_impact = 0
            projected_readiness = 100
        else:
            roadmap_impact = int(round((100 - current_readiness) * 0.95))
            projected_readiness = current_readiness + roadmap_impact

        # Calculate Success Probability
        demand_lower = demand_level.lower()
        if "very high" in demand_lower or "critical" in demand_lower:
            demand_contrib = 15.0
        elif "high" in demand_lower:
            demand_contrib = 10.0
        elif "medium" in demand_lower or "steady" in demand_lower:
            demand_contrib = 5.0
        else:
            demand_contrib = 2.0
            
        if project_count >= 2:
            portfolio_contrib = 15.0
        elif project_count == 1:
            portfolio_contrib = 8.0
        else:
            portfolio_contrib = 0.0

        success_probability = min(98, max(30, int(round(current_readiness + demand_contrib + portfolio_contrib))))

        return {
            "current_readiness": current_readiness,
            "projected_readiness": projected_readiness,
            "roadmap_completion_impact": roadmap_impact,
            "success_probability": success_probability
        }
