"""Database session management - JSON storage version."""
from app.db.json_storage import storage


class JSONSession:
    """JSON storage session (compatible with SQLAlchemy session interface)."""

    def __init__(self):
        self.storage = storage

    def add(self, obj):
        """Add object to session."""
        # Objects are added directly via storage methods
        pass

    def commit(self):
        """Commit changes (auto-saved in JSON storage)."""
        pass

    def flush(self):
        """Flush changes."""
        pass

    def refresh(self, obj):
        """Refresh object from storage."""
        pass

    def query(self, model_class):
        """Create a query object."""
        return JSONQuery(model_class, self.storage)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class JSONQuery:
    """Query interface compatible with SQLAlchemy."""

    def __init__(self, model_class, storage):
        self.model_class = model_class
        self.storage = storage
        self._filters = {}
        self._order_by = None

    def filter(self, *args):
        """Add filter conditions."""
        # Simple filter support - parse basic conditions
        for condition in args:
            # Handle simple equality filters like Model.field == value
            if hasattr(condition, "left") and hasattr(condition, "right"):
                field_name = condition.left.key if hasattr(condition.left, "key") else str(condition.left)
                value = condition.right.value if hasattr(condition.right, "value") else condition.right
                self._filters[field_name] = value
        return self

    def order_by(self, *args):
        """Add ordering."""
        if args:
            self._order_by = args[0]
        return self

    def first(self):
        """Get first result."""
        results = self.all()
        return results[0] if results else None

    def all(self):
        """Get all results."""
        table_name = self.model_class.__tablename__
        results = self.storage.query(table_name, **self._filters)

        # Apply ordering
        if self._order_by:
            field_name = self._order_by.key if hasattr(self._order_by, "key") else str(self._order_by)
            reverse = False
            if hasattr(self._order_by, "desc"):
                reverse = True
            results.sort(key=lambda x: x.get(field_name, 0), reverse=reverse)

        # Convert to model instances
        return [self._dict_to_model(r) for r in results]

    def _dict_to_model(self, data: dict):
        """Convert dictionary to model instance."""
        # Create a simple object that behaves like the model
        obj = type("ModelInstance", (), {})()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj


def get_db():
    """Get database session (JSON storage)."""
    yield JSONSession()
