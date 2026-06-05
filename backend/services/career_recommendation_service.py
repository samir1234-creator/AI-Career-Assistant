import json
import logging
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from domain.schemas.career import CareerRecommendationRequest, CareerRecommendation

logger = logging.getLogger(__name__)

class CareerRecommendationService:
    def __init__(self, db_path: Optional[str] = None):
        """
        Initializes the Career Recommendation Service and loads the careers database.
        """
        if db_path is None:
            current_dir = Path(__file__).resolve().parent
            db_path = str(current_dir.parent / "core" / "career_database.json")
            
        self.db_path = db_path
        self.career_db: Dict[str, Dict[str, Any]] = {}
        self._load_database()

    def _load_database(self) -> None:
        """
        Loads the careers database JSON file. Supports both list and dictionary formats.
        """
        try:
            if not os.path.exists(self.db_path):
                logger.warning(f"Career database not found at: {self.db_path}. Using empty database.")
                return

            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.career_db = {item["career_name"]: item for item in data}
                else:
                    self.career_db = data
                
            logger.info(f"Loaded career database. Total roles: {len(self.career_db)}")
        except Exception as e:
            logger.error(f"Failed to load career database: {str(e)}")
            self.career_db = {}

    def _is_match(self, sub: str, parent: str) -> bool:
        """
        Robust whole-word/token-based substring matching that handles programming
        languages and symbols like C++, C#, Node.js, and .NET.
        """
        db_s = sub.strip().lower()
        cand_s = parent.strip().lower()
        if db_s == cand_s:
            return True
        
        # Find all occurrences of db_s in cand_s
        start = 0
        while True:
            idx = cand_s.find(db_s, start)
            if idx == -1:
                return False
            
            # Check boundary before
            boundary_before = True
            if idx > 0:
                char_before = cand_s[idx - 1]
                if char_before.isalnum() or char_before in "+#.-":
                    boundary_before = False
                    
            # Check boundary after
            boundary_after = True
            end_idx = idx + len(db_s)
            if end_idx < len(cand_s):
                char_after = cand_s[end_idx]
                if char_after.isalnum() or char_after in "+#.-":
                    boundary_after = False
                    
            if boundary_before and boundary_after:
                return True
                
            start = idx + 1

    def _get_derived_keywords(self, role: str, category: str) -> List[str]:
        """
        Dynamically generates a list of lowercase keywords for a role and category,
        excluding generic professional words to prevent false matching.
        """
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
        
        # Add individual words of length >= 2 not in generic_words
        for word in re.findall(r'\b\w+\b', role.lower() + " " + category.lower()):
            if len(word) >= 2 and word not in generic_words:
                keywords.append(word)
                
        return list(set(keywords))

    def calculate_recommendations(self, data: CareerRecommendationRequest) -> List[CareerRecommendation]:
        """
        Calculates match scores for all careers in the database and returns the top 5 sorted recommendations.
        Uses the unified Career Intelligence Scoring Engine.
        """
        from services.career_scoring_engine import CareerScoringEngine
        results_with_scores = []
        generic_skills_lower = {"python", "java", "c++", "c#", "sql", "git", "docker", "kubernetes", "linux", "html5", "css3", "javascript", "typescript", "it", "excel"}
        
        for role, metadata in self.career_db.items():
            required_skills = metadata.get("required_skills", [])
            preferred_skills = metadata.get("preferred_skills", [])
            role_category = metadata.get("category", "")
            description = metadata.get("description", "")
            difficulty_level = metadata.get("difficulty_level", "Medium")
            growth_level = metadata.get("growth_level", "Medium")
            future_demand = metadata.get("future_demand", "Medium")
            related_careers = metadata.get("related_careers", [])
            required_keywords = metadata.get("required_keywords", [])
            
            # Derive keywords dynamically
            derived_keywords = self._get_derived_keywords(role, role_category)
            
            # Filter out generic skills from being matched in projects/certifications
            non_generic_req_skills = [s for s in required_skills if s.lower() not in generic_skills_lower]
            non_generic_pref_skills = [s for s in preferred_skills if s.lower() not in generic_skills_lower]
            
            # Identify matched and missing required/preferred skills
            matched_req = []
            for skill in required_skills:
                if any(self._is_match(skill, cand_skill) for cand_skill in data.skills):
                    matched_req.append(skill)
                    
            matched_pref = []
            for skill in preferred_skills:
                if any(self._is_match(skill, cand_skill) for cand_skill in data.skills):
                    matched_pref.append(skill)

            matched_skills_names = matched_req + matched_pref
            missing_skills_names = [s for s in required_skills + preferred_skills if s not in matched_skills_names]

            # Filter relevant projects
            relevant_projects = []
            for p_desc in data.projects:
                if (self._is_match(role, p_desc) or 
                    self._is_match(role_category, p_desc) or
                    any(self._is_match(kw, p_desc) for kw in derived_keywords + required_keywords + non_generic_req_skills + non_generic_pref_skills)):
                    relevant_projects.append(p_desc)
                    
            # Filter relevant certifications
            relevant_certs = []
            for cert_desc in data.certifications:
                if (self._is_match(role, cert_desc) or 
                    self._is_match(role_category, cert_desc) or
                    any(self._is_match(kw, cert_desc) for kw in derived_keywords + required_keywords + non_generic_req_skills + non_generic_pref_skills)):
                    relevant_certs.append(cert_desc)

            # Delegate to unified CareerScoringEngine
            scores = CareerScoringEngine.calculate_scores(
                career_name=role,
                matched_skills=matched_skills_names,
                missing_skills=missing_skills_names,
                projects=relevant_projects,
                certifications=relevant_certs,
                education=data.education,
                ats_score=data.ats_score,
                demand_level=future_demand
            )
            
            match_score = scores["current_readiness"]
            
            # Generate reasoning explanation
            reasons = []
            for s in matched_req:
                reasons.append(f"{s} detected")
            for s in matched_pref:
                reasons.append(f"{s} detected")
            if relevant_projects:
                reasons.append("Relevant project experience found")
            if relevant_certs:
                reasons.append("Relevant certification listed")
            
            # STEM alignment
            has_stem = False
            stem_keywords = ["computer science", "software", "engineering", "information technology", "mathematics", "statistics", "it"]
            for edu_desc in data.education:
                for keyword in stem_keywords:
                    if self._is_match(keyword, edu_desc):
                        has_stem = True
                        break
            if has_stem:
                reasons.append("STEM-aligned educational background")
            elif data.education:
                reasons.append("Educational background documented")
            if data.ats_score >= 70:
                reasons.append("Strong overall ATS score")
                
            unique_reasons = []
            for r in reasons:
                if r not in unique_reasons:
                    unique_reasons.append(r)
            final_reasons = unique_reasons[:4]
            if not final_reasons:
                final_reasons = ["Skills and profile show general technical alignment"]

            # Disqualify if no skill matches and no projects/certs match
            if len(matched_skills_names) == 0 and len(relevant_projects) == 0 and len(relevant_certs) == 0:
                match_score = 0

            rec = CareerRecommendation(
                role=role,
                category=role_category,
                description=description,
                match_score=match_score,
                reason=final_reasons,
                difficulty_level=difficulty_level,
                growth_level=growth_level,
                future_demand=future_demand,
                related_careers=related_careers,
                required_skills=required_skills,
                preferred_skills=preferred_skills
            )
            results_with_scores.append((match_score, rec))
            
        # Sort recommendations by match score descending, then by role name alphabetically
        results_with_scores.sort(key=lambda x: (-x[0], x[1].role))
        recommendations = [x[1] for x in results_with_scores]
        
        # Return top 5 recommendations
        return recommendations[:5]
            
        # Sort recommendations by float score descending, then by role name alphabetically
        results_with_scores.sort(key=lambda x: (-x[0], x[1].role))
        recommendations = [x[1] for x in results_with_scores]
        
        # Return top 5 recommendations
        return recommendations[:5]
