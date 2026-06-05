import json
import logging
import os
import uuid
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class RoadmapShareService:
    """
    Persists shared roadmaps as a JSON file on disk.
    Maps unique share_id → roadmap payload dict.
    Suitable for development/demo; swap with a DB for production.
    """

    def __init__(self, store_path: Optional[str] = None):
        if store_path is None:
            current_dir = Path(__file__).resolve().parent
            uploads_dir = current_dir.parent / "uploads"
            uploads_dir.mkdir(parents=True, exist_ok=True)
            store_path = str(uploads_dir / "shared_roadmaps.json")

        self.store_path = store_path
        self._store: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load existing share data from disk."""
        try:
            if os.path.exists(self.store_path):
                with open(self.store_path, "r", encoding="utf-8") as f:
                    self._store = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load share store: {e}")
            self._store = {}

    def _persist(self) -> None:
        """Save current share data to disk."""
        try:
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(self._store, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to persist share store: {e}")

    def create_share(self, roadmap_data: Dict[str, Any], candidate_name: Optional[str] = None) -> str:
        """
        Store the roadmap and return a unique share_id (8-character UUID fragment).
        """
        share_id = uuid.uuid4().hex[:12]
        self._store[share_id] = {
            "roadmap": roadmap_data,
            "candidate_name": candidate_name or "Anonymous",
        }
        self._persist()
        logger.info(f"Roadmap shared with ID: {share_id}")
        return share_id

    def get_share(self, share_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve shared roadmap by ID. Returns None if not found.
        """
        # Reload from disk in case another process updated it
        self._load()
        return self._store.get(share_id)
