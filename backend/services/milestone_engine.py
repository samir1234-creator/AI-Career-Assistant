import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class MilestoneProgressEngine:
    def __init__(self, templates_path: Optional[str] = None, dependency_path: Optional[str] = None):
        """
        Initializes the Milestone Progress Engine and loads sequencing rules & dependencies.
        """
        current_dir = Path(__file__).resolve().parent
        if templates_path is None:
            templates_path = str(current_dir.parent / "core" / "milestone_templates.json")
        if dependency_path is None:
            dependency_path = str(current_dir.parent / "core" / "skill_dependency_database.json")
            
        self.templates_path = templates_path
        self.dependency_path = dependency_path
        
        self.templates: Dict[str, List[Dict[str, Any]]] = {}
        self.dependency_db: Dict[str, List[str]] = {}
        
        self._load_databases()

    def _load_databases(self) -> None:
        try:
            if os.path.exists(self.templates_path):
                with open(self.templates_path, "r", encoding="utf-8") as f:
                    self.templates = json.load(f)
            
            if os.path.exists(self.dependency_path):
                with open(self.dependency_path, "r", encoding="utf-8") as f:
                    self.dependency_db = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load milestone engine databases: {str(e)}")

    def _get_skill_depth(self, skill: str, missing_set: set, memo: dict) -> int:
        skill_lower = skill.lower().strip()
        if skill_lower in memo:
            return memo[skill_lower]
            
        # Get prerequisites in dependency database
        prereqs = []
        for k, dep_list in self.dependency_db.items():
            if k.lower().strip() == skill_lower:
                prereqs = dep_list
                break
                
        # Filter prerequisites to only include other missing skills
        missing_prereqs = [p for p in prereqs if p.lower().strip() in missing_set]
        
        if not missing_prereqs:
            memo[skill_lower] = 0
            return 0
            
        # Recursively find maximum depth
        max_depth = 0
        for p in missing_prereqs:
            max_depth = max(max_depth, self._get_skill_depth(p, missing_set, memo))
            
        memo[skill_lower] = 1 + max_depth
        return 1 + max_depth

    def generate_milestones(self, career_name: str, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Generates a milestone-based progression roadmap for learning missing skills.
        Groups skills logically and sequences them using templates or dependency resolution.
        """
        if not missing_skills:
            return [{
                "index": 1,
                "title": "Ready",
                "skills": [f"{career_name} Ready"]
            }]
            
        missing_set = {s.lower().strip() for s in missing_skills}
        missing_map = {s.lower().strip(): s for s in missing_skills}
        
        # 1. Template-based Matching
        matched_template_key = None
        for key in self.templates:
            if key.lower().strip() == career_name.lower().strip():
                matched_template_key = key
                break
                
        milestones = []
        
        if matched_template_key:
            # Group missing skills using template rules
            template_milestones = self.templates[matched_template_key]
            grouped_skills = {}  # index -> list of original skills
            
            for item in template_milestones:
                idx = item["milestone_index"]
                title = item["title"]
                t_skills = item["skills"]
                
                # Check if any template skills are missing
                missing_in_milestone = []
                for ts in t_skills:
                    ts_lower = ts.lower().strip()
                    if ts_lower in missing_set:
                        missing_in_milestone.append(missing_map[ts_lower])
                        missing_set.remove(ts_lower) # Remove to avoid duplicate placement
                        
                if missing_in_milestone:
                    grouped_skills[idx] = {
                        "title": title,
                        "skills": missing_in_milestone
                    }
                    
            # Handle any remaining missing skills (e.g. custom or optional skills not in templates)
            if missing_set:
                # Place residual skills in Milestone 1 or calculate depth
                residuals = [missing_map[s] for s in missing_set]
                if 1 in grouped_skills:
                    grouped_skills[1]["skills"].extend(residuals)
                else:
                    grouped_skills[1] = {
                        "title": "Foundations",
                        "skills": residuals
                    }
                    
            # Sort milestones by template index and re-index sequentially (1, 2, 3...)
            sorted_indices = sorted(grouped_skills.keys())
            for i, idx in enumerate(sorted_indices, start=1):
                milestones.append({
                    "index": i,
                    "title": f"Milestone {i}: {grouped_skills[idx]['title']}",
                    "skills": grouped_skills[idx]["skills"]
                })
        else:
            # 2. Dynamic Fallback Algorithm (Topological Dependency Partitioning)
            memo = {}
            skill_depths = {}
            for s in missing_skills:
                skill_depths[s] = self._get_skill_depth(s, missing_set, memo)
                
            # Group skills by depth
            depth_groups = {}
            for s, depth in skill_depths.items():
                if depth not in depth_groups:
                    depth_groups[depth] = []
                depth_groups[depth].append(s)
                
            # Sort by depth and build milestones
            sorted_depths = sorted(depth_groups.keys())
            for i, depth in enumerate(sorted_depths, start=1):
                # Formulate titles based on level
                if depth == 0:
                    title_name = "Core Foundations"
                elif depth == 1:
                    title_name = "Intermediate Concepts"
                elif depth == 2:
                    title_name = "Advanced Frameworks"
                else:
                    title_name = "Specialized Specializations"
                    
                milestones.append({
                    "index": i,
                    "title": f"Milestone {i}: {title_name}",
                    "skills": depth_groups[depth]
                })
                
        # 3. Always append final Career Ready milestone
        next_idx = len(milestones) + 1
        milestones.append({
            "index": next_idx,
            "title": f"Milestone {next_idx}: {career_name} Ready",
            "skills": [f"Ready to apply for {career_name} roles!"]
        })
        
        return milestones
