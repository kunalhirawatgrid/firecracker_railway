"""
JSON-based in-memory storage for development/testing.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading

STORAGE_DIR = Path(__file__).parent.parent.parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# Thread lock for concurrent access
_lock = threading.Lock()


class JSONStorage:
    """JSON-based storage implementation."""

    def __init__(self, filename: str = "data.json"):
        """Initialize JSON storage."""
        self.filename = STORAGE_DIR / filename
        self._data: Dict[str, List[Dict]] = {}
        self._load()

    def _load(self):
        """Load data from JSON file."""
        if self.filename.exists():
            try:
                with open(self.filename, "r") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        """Save data to JSON file."""
        with _lock:
            with open(self.filename, "w") as f:
                json.dump(self._data, f, indent=2, default=str)

    def _get_table(self, table_name: str) -> List[Dict]:
        """Get table data."""
        if table_name not in self._data:
            self._data[table_name] = []
        return self._data[table_name]

    def _get_next_id(self, table_name: str) -> int:
        """Get next ID for a table."""
        table = self._get_table(table_name)
        if not table:
            return 1
        return max(item.get("id", 0) for item in table) + 1

    def create(self, table_name: str, data: Dict) -> Dict:
        """Create a new record."""
        table = self._get_table(table_name)
        record = data.copy()
        record["id"] = self._get_next_id(table_name)
        record["created_at"] = datetime.utcnow().isoformat()
        record["updated_at"] = datetime.utcnow().isoformat()
        table.append(record)
        self._save()
        return record

    def get(self, table_name: str, record_id: int) -> Optional[Dict]:
        """Get a record by ID."""
        table = self._get_table(table_name)
        for record in table:
            if record.get("id") == record_id:
                return record
        return None

    def get_all(self, table_name: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all records, optionally filtered."""
        table = self._get_table(table_name)
        if not filters:
            return table.copy()

        result = []
        for record in table:
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                result.append(record)
        return result

    def update(self, table_name: str, record_id: int, data: Dict) -> Optional[Dict]:
        """Update a record."""
        table = self._get_table(table_name)
        for i, record in enumerate(table):
            if record.get("id") == record_id:
                updated = record.copy()
                updated.update(data)
                updated["updated_at"] = datetime.utcnow().isoformat()
                updated["id"] = record_id  # Preserve ID
                table[i] = updated
                self._save()
                return updated
        return None

    def delete(self, table_name: str, record_id: int) -> bool:
        """Delete a record."""
        table = self._get_table(table_name)
        for i, record in enumerate(table):
            if record.get("id") == record_id:
                table.pop(i)
                self._save()
                return True
        return False

    def query(self, table_name: str, **filters) -> List[Dict]:
        """Query records with multiple filters."""
        return self.get_all(table_name, filters if filters else None)

    def clear(self, table_name: Optional[str] = None):
        """Clear all data or a specific table."""
        if table_name:
            self._data[table_name] = []
        else:
            self._data = {}
        self._save()


# Global storage instance
storage = JSONStorage()

