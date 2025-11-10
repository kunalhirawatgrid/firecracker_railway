from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.assessment import Language, TestCaseType


class TestCaseResponse(BaseModel):
    id: str
    input: str
    expected_output: str
    type: str
    description: Optional[str] = None


class QuestionResponse(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    sample_test_cases: List[TestCaseResponse]
    allowed_languages: List[str]
    time_limit: int


class AssessmentResponse(BaseModel):
    id: str
    title: str
    description: str
    questions: List[QuestionResponse]
    duration: int
    created_at: datetime


class AssessmentCreate(BaseModel):
    title: str
    description: str
    questions: List[dict]
    duration: int = Field(..., gt=0, description="Duration in minutes")


class CodeExecutionRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: Language
    input: Optional[str] = None
    question_id: Optional[str] = None
    assessment_id: Optional[str] = None
    candidate_id: str = "anonymous"


class TestExecutionRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: Language
    question_id: str
    assessment_id: str
    candidate_id: str = "anonymous"
    include_hidden: bool = False


class ExecutionResultResponse(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: Optional[float] = None
    memory_used: Optional[int] = None


# Alias for backward compatibility
CodeExecutionResponse = ExecutionResultResponse


class TestResultResponse(BaseModel):
    test_case_id: str
    passed: bool
    input: str
    expected_output: str
    actual_output: str
    error: Optional[str] = None
    execution_time: Optional[float] = None


class SubmissionResponse(BaseModel):
    id: str
    assessment_id: str
    question_id: str
    candidate_id: str
    code: str
    language: str
    test_results: List[TestResultResponse]
    sample_passed: int
    sample_total: int
    hidden_passed: int
    hidden_total: int
    compilation_logs: Optional[str] = None
    submitted_at: datetime
