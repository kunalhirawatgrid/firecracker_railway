"""
JSON-compatible model definitions.
These models work with JSON storage instead of SQLAlchemy.
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum


class AssessmentStatus(str, Enum):
    """Assessment status enum."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class Assessment:
    """Assessment model for JSON storage."""
    __tablename__ = "assessments"

    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "",
        description: Optional[str] = None,
        duration_minutes: int = 60,
        candidate_id: str = "",
        status: str = AssessmentStatus.NOT_STARTED,
        started_at: Optional[str] = None,
        expires_at: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.duration_minutes = duration_minutes
        self.candidate_id = candidate_id
        self.status = status
        self.started_at = started_at
        self.expires_at = expires_at
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "candidate_id": self.candidate_id,
            "status": self.status,
            "started_at": self.started_at,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)


class Question:
    """Question model for JSON storage."""
    __tablename__ = "questions"

    def __init__(
        self,
        id: Optional[int] = None,
        assessment_id: int = 0,
        title: str = "",
        description: str = "",
        difficulty: str = "easy",
        order: int = 0,
        time_limit_minutes: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.assessment_id = assessment_id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.order = order
        self.time_limit_minutes = time_limit_minutes
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "order": self.order,
            "time_limit_minutes": self.time_limit_minutes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)


class TestCase:
    """TestCase model for JSON storage."""
    __tablename__ = "test_cases"

    def __init__(
        self,
        id: Optional[int] = None,
        question_id: int = 0,
        input_data: str = "",
        expected_output: str = "",
        is_sample: bool = False,
        order: int = 0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.question_id = question_id
        self.input_data = input_data
        self.expected_output = expected_output
        self.is_sample = is_sample
        self.order = order
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "question_id": self.question_id,
            "input_data": self.input_data,
            "expected_output": self.expected_output,
            "is_sample": self.is_sample,
            "order": self.order,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)


class Submission:
    """Submission model for JSON storage."""
    __tablename__ = "submissions"

    def __init__(
        self,
        id: Optional[int] = None,
        assessment_id: int = 0,
        question_id: int = 0,
        candidate_id: str = "",
        language: str = "python",
        code: str = "",
        status: str = "pending",
        compilation_logs: Optional[str] = None,
        execution_logs: Optional[str] = None,
        passed_test_cases: int = 0,
        total_test_cases: int = 0,
        execution_time_ms: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.assessment_id = assessment_id
        self.question_id = question_id
        self.candidate_id = candidate_id
        self.language = language
        self.code = code
        self.status = status
        self.compilation_logs = compilation_logs
        self.execution_logs = execution_logs
        self.passed_test_cases = passed_test_cases
        self.total_test_cases = total_test_cases
        self.execution_time_ms = execution_time_ms
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "question_id": self.question_id,
            "candidate_id": self.candidate_id,
            "language": self.language,
            "code": self.code,
            "status": self.status,
            "compilation_logs": self.compilation_logs,
            "execution_logs": self.execution_logs,
            "passed_test_cases": self.passed_test_cases,
            "total_test_cases": self.total_test_cases,
            "execution_time_ms": self.execution_time_ms,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)


class TestResult:
    """TestResult model for JSON storage."""
    __tablename__ = "test_results"

    def __init__(
        self,
        id: Optional[int] = None,
        submission_id: int = 0,
        test_case_id: int = 0,
        passed: bool = False,
        actual_output: Optional[str] = None,
        error_message: Optional[str] = None,
        execution_time_ms: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.submission_id = submission_id
        self.test_case_id = test_case_id
        self.passed = passed
        self.actual_output = actual_output
        self.error_message = error_message
        self.execution_time_ms = execution_time_ms
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "submission_id": self.submission_id,
            "test_case_id": self.test_case_id,
            "passed": self.passed,
            "actual_output": self.actual_output,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)

