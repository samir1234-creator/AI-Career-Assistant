import json
import logging
import os
from collections import defaultdict, deque
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

logger = logging.getLogger(__name__)


class MilestoneProgressEngine:
    def __init__(self, templates_path: Optional[str] = None, dependency_path: Optional[str] = None):
        """
        Initializes the Milestone Progress Engine with Kahn's topological sort.
        Loads sequencing rules and dependency graphs for dependency-aware ordering.
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

    def _normalize(self, skill: str) -> str:
        """Normalize skill name for comparison."""
        return skill.strip().lower()

    def _deduplicate_skills(self, skills: List[str]) -> List[str]:
        """Remove duplicate skills (case-insensitive), preserving first-seen order and original casing."""
        seen: Set[str] = set()
        result = []
        for s in skills:
            key = self._normalize(s)
            if key not in seen:
                seen.add(key)
                result.append(s)
        return result

    def _build_dependency_graph(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Build a directed adjacency list for skills: prerequisite → skill.
        Only includes edges where BOTH prerequisite and skill are in the provided list.
        """
        skill_set = {self._normalize(s) for s in skills}
        skill_map = {self._normalize(s): s for s in skills}  # normalized → original

        graph: Dict[str, List[str]] = defaultdict(list)  # prereq_norm → [dependent_norm]
        in_degree: Dict[str, int] = {self._normalize(s): 0 for s in skills}

        for k, prereqs in self.dependency_db.items():
            k_norm = self._normalize(k)
            if k_norm not in skill_set:
                continue
            for prereq in prereqs:
                prereq_norm = self._normalize(prereq)
                if prereq_norm in skill_set:
                    graph[prereq_norm].append(k_norm)
                    in_degree[k_norm] = in_degree.get(k_norm, 0) + 1

        return graph, in_degree, skill_map

    def _topological_sort_kahn(self, skills: List[str]) -> List[str]:
        """
        Kahn's BFS topological sort on the skill dependency graph.
        Returns skills ordered from foundational (prerequisites first) to advanced.
        Skills with no dependencies come first; skills dependent on others come after.
        """
        if not skills:
            return []

        deduped = self._deduplicate_skills(skills)
        graph, in_degree, skill_map = self._build_dependency_graph(deduped)

        # Start with all skills that have in_degree == 0 (no prerequisites in this skill set)
        queue = deque()
        for s_norm, deg in in_degree.items():
            if deg == 0:
                queue.append(s_norm)

        # Sort queue initially alphabetically for deterministic output
        queue = deque(sorted(queue))

        sorted_norms = []
        while queue:
            node = queue.popleft()
            sorted_norms.append(node)
            for neighbor in sorted(graph[node]):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Handle cycles (if any) — append remaining nodes at the end
        remaining = [n for n in in_degree if in_degree[n] > 0]
        sorted_norms.extend(sorted(remaining))

        # Restore original casing
        return [skill_map.get(n, n) for n in sorted_norms]

    def generate_milestones(self, career_name: str, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Generates a dependency-aware milestone progression roadmap.
        Always sorts skills using Kahn's topological sort first, then places
        them in templates or fallback depth-based milestones.
        """
        if not missing_skills:
            return [{
                "index": 1,
                "title": f"Milestone 1: {career_name} Ready",
                "skills": [f"{career_name} Ready"]
            }]

        # Deduplicate missing skills (case-insensitive)
        deduped_missing = self._deduplicate_skills(missing_skills)
        missing_set = {self._normalize(s) for s in deduped_missing}
        missing_map = {self._normalize(s): s for s in deduped_missing}

        # ALWAYS perform Kahn's topological sort first
        sorted_skills = self._topological_sort_kahn(deduped_missing)

        milestones = []

        # --- Template-Based Matching ---
        matched_template_key = None
        for key in self.templates:
            if self._normalize(key) == self._normalize(career_name):
                matched_template_key = key
                break

        if matched_template_key:
            template_milestones = self.templates[matched_template_key]
            grouped: Dict[int, Dict[str, Any]] = {}

            # Map normalized skill name to its milestone index and title in the template
            skill_to_template_milestone: Dict[str, Tuple[int, str]] = {}
            for item in template_milestones:
                idx = item["milestone_index"]
                title = item["title"]
                for ts in item["skills"]:
                    skill_to_template_milestone[self._normalize(ts)] = (idx, title)

            # Place each sorted skill into its corresponding template milestone
            for skill in sorted_skills:
                skill_norm = self._normalize(skill)
                if skill_norm in skill_to_template_milestone:
                    idx, title = skill_to_template_milestone[skill_norm]
                    if idx not in grouped:
                        grouped[idx] = {
                            "title": title,
                            "skills": []
                        }
                    grouped[idx]["skills"].append(skill)
                else:
                    # Place residual skill in the first milestone
                    first_idx = 1
                    first_title = template_milestones[0]["title"] if template_milestones else "Foundations"
                    if first_idx not in grouped:
                        grouped[first_idx] = {
                            "title": first_title,
                            "skills": []
                        }
                    grouped[first_idx]["skills"].append(skill)

            # Sort by template index, re-index sequentially
            for i, idx in enumerate(sorted(grouped.keys()), start=1):
                milestones.append({
                    "index": i,
                    "title": f"Milestone {i}: {grouped[idx]['title']}",
                    "skills": grouped[idx]["skills"]
                })

        else:
            # --- Dynamic Fallback: Kahn's Topological Sort ---
            # Group into milestones of ~2-3 skills each based on dependency depth
            # First, compute depth of each skill
            memo: Dict[str, int] = {}
            depth_map: Dict[str, int] = {}
            for s in sorted_skills:
                depth_map[s] = self._get_skill_depth(s, missing_set, memo)

            depth_groups: Dict[int, List[str]] = defaultdict(list)
            for s, d in depth_map.items():
                depth_groups[d].append(s)

            title_map = {
                0: "Core Foundations",
                1: "Intermediate Concepts",
                2: "Advanced Frameworks",
                3: "Specialized Topics"
            }

            for i, depth in enumerate(sorted(depth_groups.keys()), start=1):
                t_name = title_map.get(depth, f"Level {depth + 1} Skills")
                milestones.append({
                    "index": i,
                    "title": f"Milestone {i}: {t_name}",
                    "skills": depth_groups[depth]
                })

        # Always append final Career Ready milestone
        next_idx = len(milestones) + 1
        milestones.append({
            "index": next_idx,
            "title": f"Milestone {next_idx}: {career_name} Ready",
            "skills": [f"Ready to apply for {career_name} roles!"]
        })

        return milestones

    def _get_skill_depth(self, skill: str, missing_set: set, memo: dict) -> int:
        """Recursively computes skill depth within the missing skill dependency graph."""
        skill_lower = self._normalize(skill)
        if skill_lower in memo:
            return memo[skill_lower]

        prereqs = []
        for k, dep_list in self.dependency_db.items():
            if self._normalize(k) == skill_lower:
                prereqs = dep_list
                break

        missing_prereqs = [p for p in prereqs if self._normalize(p) in missing_set]

        if not missing_prereqs:
            memo[skill_lower] = 0
            return 0

        max_depth = max(self._get_skill_depth(p, missing_set, memo) for p in missing_prereqs)
        memo[skill_lower] = 1 + max_depth
        return 1 + max_depth
