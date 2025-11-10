from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Language(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    JAVASCRIPT = "javascript"


class TestCaseType(str, Enum):
    SAMPLE = "sample"
    HIDDEN = "hidden"


class TestCase:
    def __init__(
        self,
        id: str,
        input: str,
        expected_output: str,
        type: TestCaseType,
        description: Optional[str] = None
    ):
        self.id = id
        self.input = input
        self.expected_output = expected_output
        self.type = type
        self.description = description


class Question:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        difficulty: str,
        sample_test_cases: List[TestCase],
        hidden_test_cases: List[TestCase],
        allowed_languages: List[Language],
        time_limit: int = 60,  # minutes
    ):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.sample_test_cases = sample_test_cases
        self.hidden_test_cases = hidden_test_cases
        self.allowed_languages = allowed_languages
        self.time_limit = time_limit


class Assessment:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        questions: List[Question],
        duration: int,  # minutes
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.questions = questions
        self.duration = duration
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "questions": [
                {
                    "id": q.id,
                    "title": q.title,
                    "description": q.description,
                    "difficulty": q.difficulty,
                    "sample_test_cases": [
                        {
                            "id": tc.id,
                            "input": tc.input,
                            "expected_output": tc.expected_output,
                            "type": tc.type.value,
                            "description": tc.description,
                        }
                        for tc in q.sample_test_cases
                    ],
                    "hidden_test_cases": [
                        {
                            "id": tc.id,
                            "input": tc.input,
                            "expected_output": tc.expected_output,
                            "type": tc.type.value,
                            "description": tc.description,
                        }
                        for tc in q.hidden_test_cases
                    ],
                    "allowed_languages": [lang.value for lang in q.allowed_languages],
                    "time_limit": q.time_limit,
                }
                for q in self.questions
            ],
            "duration": self.duration,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Assessment":
        questions = []
        for q_data in data["questions"]:
            sample_tcs = [
                TestCase(
                    id=tc["id"],
                    input=tc["input"],
                    expected_output=tc["expected_output"],
                    type=TestCaseType(tc["type"]),
                    description=tc.get("description"),
                )
                for tc in q_data["sample_test_cases"]
            ]
            hidden_tcs = [
                TestCase(
                    id=tc["id"],
                    input=tc["input"],
                    expected_output=tc["expected_output"],
                    type=TestCaseType(tc["type"]),
                    description=tc.get("description"),
                )
                for tc in q_data["hidden_test_cases"]
            ]
            question = Question(
                id=q_data["id"],
                title=q_data["title"],
                description=q_data["description"],
                difficulty=q_data["difficulty"],
                sample_test_cases=sample_tcs,
                hidden_test_cases=hidden_tcs,
                allowed_languages=[Language(lang) for lang in q_data["allowed_languages"]],
                time_limit=q_data.get("time_limit", 60),
            )
            questions.append(question)
        
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            questions=questions,
            duration=data["duration"],
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
        )


class ExecutionResult:
    def __init__(
        self,
        success: bool,
        output: str,
        error: Optional[str] = None,
        execution_time: Optional[float] = None,
        memory_used: Optional[int] = None,
    ):
        self.success = success
        self.output = output
        self.error = error
        self.execution_time = execution_time
        self.memory_used = memory_used


class TestResult:
    def __init__(
        self,
        test_case_id: str,
        passed: bool,
        input: str,
        expected_output: str,
        actual_output: str,
        error: Optional[str] = None,
        execution_time: Optional[float] = None,
    ):
        self.test_case_id = test_case_id
        self.passed = passed
        self.input = input
        self.expected_output = expected_output
        self.actual_output = actual_output
        self.error = error
        self.execution_time = execution_time


class Submission:
    def __init__(
        self,
        id: str,
        assessment_id: str,
        question_id: str,
        candidate_id: str,
        code: str,
        language: Language,
        test_results: List[TestResult],
        sample_passed: int,
        sample_total: int,
        hidden_passed: int,
        hidden_total: int,
        compilation_logs: Optional[str] = None,
        submitted_at: Optional[datetime] = None,
    ):
        self.id = id
        self.assessment_id = assessment_id
        self.question_id = question_id
        self.candidate_id = candidate_id
        self.code = code
        self.language = language
        self.test_results = test_results
        self.sample_passed = sample_passed
        self.sample_total = sample_total
        self.hidden_passed = hidden_passed
        self.hidden_total = hidden_total
        self.compilation_logs = compilation_logs
        self.submitted_at = submitted_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "question_id": self.question_id,
            "candidate_id": self.candidate_id,
            "code": self.code,
            "language": self.language.value,
            "test_results": [
                {
                    "test_case_id": tr.test_case_id,
                    "passed": tr.passed,
                    "input": tr.input,
                    "expected_output": tr.expected_output,
                    "actual_output": tr.actual_output,
                    "error": tr.error,
                    "execution_time": tr.execution_time,
                }
                for tr in self.test_results
            ],
            "sample_passed": self.sample_passed,
            "sample_total": self.sample_total,
            "hidden_passed": self.hidden_passed,
            "hidden_total": self.hidden_total,
            "compilation_logs": self.compilation_logs,
            "submitted_at": self.submitted_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Submission":
        from app.models.assessment import TestResult
        test_results = [
            TestResult(
                test_case_id=tr["test_case_id"],
                passed=tr["passed"],
                input=tr["input"],
                expected_output=tr["expected_output"],
                actual_output=tr["actual_output"],
                error=tr.get("error"),
                execution_time=tr.get("execution_time"),
            )
            for tr in data["test_results"]
        ]
        return cls(
            id=data["id"],
            assessment_id=data["assessment_id"],
            question_id=data["question_id"],
            candidate_id=data["candidate_id"],
            code=data["code"],
            language=Language(data["language"]),
            test_results=test_results,
            sample_passed=data["sample_passed"],
            sample_total=data["sample_total"],
            hidden_passed=data["hidden_passed"],
            hidden_total=data["hidden_total"],
            compilation_logs=data.get("compilation_logs"),
            submitted_at=datetime.fromisoformat(data["submitted_at"]) if data.get("submitted_at") else None,
        )

