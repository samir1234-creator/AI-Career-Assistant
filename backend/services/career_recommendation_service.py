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
        Uses upgraded weighted scoring:
        - 40% Skill Match
        - 20% Project Relevance
        - 10% Certification Relevance
        - 10% Education Relevance
        - 10% ATS Score
        - 10% Career Demand
        """
        results_with_scores = []
        generic_skills_lower = {"python", "java", "c++", "c#", "sql", "git", "docker", "kubernetes", "linux", "html5", "css3", "javascript", "typescript", "it", "excel"}
        
        for role, metadata in self.career_db.items():
            score = 0.0
            reasons = []
            
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
            
            # 1. Skill Match (max 40 points)
            # Use 10.0 points per required match and 6.0 points per preferred match to balance general software roles
            matched_req = 0
            for skill in required_skills:
                if any(self._is_match(skill, cand_skill) for cand_skill in data.skills):
                    matched_req += 1
                    reasons.append(f"{skill} detected")
            req_score = min(matched_req * 10.0, 28.0)
                
            matched_pref = 0
            for skill in preferred_skills:
                if any(self._is_match(skill, cand_skill) for cand_skill in data.skills):
                    matched_pref += 1
                    reasons.append(f"{skill} detected")
            pref_score = min(matched_pref * 6.0, 12.0)
                
            score += (req_score + pref_score)
            
            # 2. Project Relevance (max 20 points)
            project_score = 0.0
            has_relevant_project = False
            
            # Check for direct match (20 points)
            for p_desc in data.projects:
                if self._is_match(role, p_desc) or self._is_match(role_category, p_desc):
                    project_score = 20.0
                    has_relevant_project = True
                    break
                    
            # Check for keyword/non-generic skill match (15 points)
            if not has_relevant_project:
                for p_desc in data.projects:
                    # Match derived keywords, required_keywords, or domain-specific required/preferred skills
                    if any(self._is_match(kw, p_desc) for kw in derived_keywords + required_keywords + non_generic_req_skills + non_generic_pref_skills):
                        project_score = 15.0
                        has_relevant_project = True
                        break
                        
            score += project_score
            if has_relevant_project:
                reasons.append("Relevant project experience found")
                
            # 3. Certification Relevance (max 10 points)
            cert_score = 0.0
            has_relevant_cert = False
            
            # Check for direct match (10 points)
            for cert_desc in data.certifications:
                if self._is_match(role, cert_desc) or self._is_match(role_category, cert_desc):
                    cert_score = 10.0
                    has_relevant_cert = True
                    break
                    
            # Check for keyword/non-generic skill match (8 points)
            if not has_relevant_cert:
                for cert_desc in data.certifications:
                    if any(self._is_match(kw, cert_desc) for kw in derived_keywords + required_keywords + non_generic_req_skills + non_generic_pref_skills):
                        cert_score = 8.0
                        has_relevant_cert = True
                        break
                        
            score += cert_score
            if has_relevant_cert:
                reasons.append("Relevant certification listed")
                
            # 4. Education Relevance (max 10 points)
            edu_score = 0.0
            has_stem = False
            stem_keywords = ["computer science", "software", "engineering", "information technology", "mathematics", "statistics", "it"]
            
            if data.education:
                for edu_desc in data.education:
                    for keyword in stem_keywords:
                        if self._is_match(keyword, edu_desc):
                            has_stem = True
                            break
                    if has_stem:
                        break
                edu_score = 10.0 if has_stem else 7.0
            score += edu_score
            if has_stem:
                reasons.append("STEM-aligned educational background")
            elif data.education:
                reasons.append("Educational background documented")
                
            # 5. ATS Score Weight (max 10 points)
            ats_contrib = (data.ats_score / 100.0) * 10.0
            score += ats_contrib
            if data.ats_score >= 70:
                reasons.append("Strong overall ATS score")
                
            # 6. Career Demand (max 10 points)
            demand_score = 7.0
            if future_demand.lower() == "high":
                demand_score = 10.0
            elif future_demand.lower() == "low":
                demand_score = 4.0
            score += demand_score
            
            score_float = score
            
            # Disqualify/heavily penalize roles with absolutely zero domain match to improve matching realism
            if matched_req == 0 and matched_pref == 0 and not has_relevant_project and not has_relevant_cert:
                score_float = 0.0
                
            # Cap final score float at 100
            score_float = min(score_float, 100.0)
            
            # Add match ratio tie-breaker to favor candidates with higher coverage of required skills
            if required_skills:
                score_float += (matched_req / len(required_skills)) * 2.0
            
            # Deduplicate reasons list
            unique_reasons = []
            for r in reasons:
                if r not in unique_reasons:
                    unique_reasons.append(r)
                    
            # Cap reasons at top 4
            final_reasons = unique_reasons[:4]
            if not final_reasons:
                final_reasons = ["Skills and profile show general technical alignment"]
                
            rec = CareerRecommendation(
                role=role,
                category=role_category,
                description=description,
                match_score=int(round(min(score_float, 100.0))),
                reason=final_reasons,
                difficulty_level=difficulty_level,
                growth_level=growth_level,
                future_demand=future_demand,
                related_careers=related_careers,
                required_skills=required_skills,
                preferred_skills=preferred_skills
            )
            results_with_scores.append((score_float, rec))
            
        # Sort recommendations by float score descending, then by role name alphabetically
        results_with_scores.sort(key=lambda x: (-x[0], x[1].role))
        recommendations = [x[1] for x in results_with_scores]
        
        # Return top 5 recommendations
        return recommendations[:5]
