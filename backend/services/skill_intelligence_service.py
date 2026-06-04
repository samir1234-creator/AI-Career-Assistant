import json
import logging
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# Mapping from database categories (plural) to API expected singular categories
SINGULAR_CATEGORIES = {
    "Programming Languages": "Programming Language",
    "Frontend Frameworks": "Frontend Framework",
    "Backend Frameworks": "Backend Framework",
    "Databases": "Database",
    "Cloud Computing": "Cloud Computing",
    "DevOps": "DevOps",
    "Artificial Intelligence": "Artificial Intelligence",
    "Data Science": "Data Science",
    "Mobile Development": "Mobile Development",
    "Tools & Technologies": "Tools & Technologies"
}

class SkillIntelligenceService:
    def __init__(self, db_path: Optional[str] = None):
        """
        Initializes the Skill Intelligence Service and loads the skills database.
        """
        if db_path is None:
            # Resolve default path relative to this file: backend/core/skills_database.json
            current_dir = Path(__file__).resolve().parent
            db_path = str(current_dir.parent / "core" / "skills_database.json")
            
        self.db_path = db_path
        self.skills_db: Dict[str, List[str]] = {}
        self.lookup_map: Dict[str, Tuple[str, str]] = {} # lowercase_skill -> (canonical_name, category)
        self._load_database()

    def _load_database(self) -> None:
        """
        Loads the skills database JSON file and constructs a fast lookup index.
        """
        try:
            if not os.path.exists(self.db_path):
                logger.warning(f"Skills database not found at: {self.db_path}. Using empty database.")
                return

            with open(self.db_path, "r", encoding="utf-8") as f:
                self.skills_db = json.load(f)
                
            # Build lookup map: lowercase skill name -> (canonical name, category)
            for category, skills in self.skills_db.items():
                for skill in skills:
                    normalized_skill = self._normalize_name(skill)
                    if normalized_skill:
                        self.lookup_map[normalized_skill] = (skill, category)
                        
            logger.info(f"Loaded skills database. Categories: {len(self.skills_db)}, Indexed skills: {len(self.lookup_map)}")
        except Exception as e:
            logger.error(f"Failed to load skills database: {str(e)}")
            self.skills_db = {}
            self.lookup_map = {}

    def _normalize_name(self, name: str) -> str:
        """
        Normalizes a skill name by trimming, replacing multiple spaces with a single space, and lowercasing.
        This helps in robust multi-word matching.
        """
        if not name:
            return ""
        # Replace multiple spaces/tabs with single space, lowercase and strip
        return re.sub(r'\s+', ' ', name.strip()).lower()

    def lookup_skill(self, skill_name: str) -> Tuple[str, str]:
        """
        Performs a case-insensitive, space-normalized lookup in the skills database.
        Returns:
            Tuple[str, str]: (category, canonical_name)
            If not found, returns ("Other", skill_name)
        """
        normalized = self._normalize_name(skill_name)
        if normalized in self.lookup_map:
            canonical_name, category = self.lookup_map[normalized]
            return category, canonical_name
        return "Other", skill_name

    def classify_skills(self, skills: List[str]) -> List[Dict[str, str]]:
        """
        Classifies a list of skill strings.
        Handles duplicates, normalizes casing, processes multi-word entries, and assigns a category.
        
        Args:
            skills: List of skill strings to categorize.
            
        Returns:
            List of dicts representing enriched skills: [{"name": "...", "category": "..."}]
        """
        seen_normalized = set()
        enriched_skills = []

        for raw_skill in skills:
            if not raw_skill:
                continue
                
            skill_trimmed = raw_skill.strip()
            normalized = self._normalize_name(skill_trimmed)
            
            if not normalized:
                continue
                
            # Duplicate removal: ignore if we have already processed this normalized skill
            if normalized in seen_normalized:
                continue
            seen_normalized.add(normalized)
            
            category, canonical_name = self.lookup_skill(skill_trimmed)
            
            # Map category to API expected singular format (e.g. Programming Language)
            api_category = SINGULAR_CATEGORIES.get(category, category)
            
            enriched_skills.append({
                "name": canonical_name,
                "category": api_category
            })
            
        return enriched_skills
