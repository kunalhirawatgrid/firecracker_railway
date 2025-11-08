"""Assessment schemas."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class TestCaseBase(BaseModel):
    """Base test case schema."""
    input_data: str
    expected_output: str
    is_sample: bool = False
    order: int = 0


class TestCaseCreate(TestCaseBase):
    """Test case creation schema."""
    pass


class TestCaseResponse(TestCaseBase):
    """Test case response schema."""
    id: int
    
    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    """Base question schema."""
    title: str
    description: str
    difficulty: str
    order: int = 0
    time_limit_minutes: Optional[int] = None


class QuestionCreate(QuestionBase):
    """Question creation schema."""
    test_cases: List[TestCaseCreate] = []


class QuestionResponse(QuestionBase):
    """Question response schema."""
    id: int
    assessment_id: int
    test_cases: List[TestCaseResponse] = []
    
    class Config:
        from_attributes = True


class AssessmentBase(BaseModel):
    """Base assessment schema."""
    title: str
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0)


class AssessmentCreate(AssessmentBase):
    """Assessment creation schema."""
    candidate_id: str
    questions: List[QuestionCreate] = []


class AssessmentResponse(AssessmentBase):
    """Assessment response schema."""
    id: int
    candidate_id: str
    status: str
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    questions: List[QuestionResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssessmentStart(BaseModel):
    """Assessment start request."""
    candidate_id: str


class CodeExecutionRequest(BaseModel):
    """Code execution request."""
    code: str = Field(..., max_length=50000)
    language: str = Field(..., pattern="^(python|java|cpp|javascript)$")
    input_data: Optional[str] = None


class CodeExecutionResponse(BaseModel):
    """Code execution response."""
    success: bool
    stdout: str
    stderr: str
    execution_time_ms: int
    return_code: Optional[int] = None
    error: Optional[str] = None


class TestResultResponse(BaseModel):
    """Test result response."""
    test_case_id: int
    is_sample: bool
    passed: bool
    actual_output: Optional[str] = None
    expected_output: Optional[str] = None
    error: Optional[str] = None
    execution_time_ms: int


class SubmissionRequest(BaseModel):
    """Submission request."""
    code: str = Field(..., max_length=50000)
    language: str = Field(..., pattern="^(python|java|cpp|javascript)$")


class SubmissionResponse(BaseModel):
    """Submission response."""
    id: int
    question_id: int
    language: str
    status: str
    passed_test_cases: int
    total_test_cases: int
    compilation_logs: Optional[str] = None
    execution_logs: Optional[str] = None
    execution_time_ms: Optional[int] = None
    test_results: List[TestResultResponse] = []
    created_at: datetime
    
    class Config:
        from_attributes = True

