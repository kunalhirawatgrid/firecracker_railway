from fastapi import APIRouter, HTTPException
from typing import Optional
import uuid
from datetime import datetime
from app.schemas.assessment import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    SubmissionResponse,
    TestExecutionRequest,
)
from app.models.assessment import Language, Submission, TestCaseType
from app.services.code_executor import code_executor_service
from app.db.json_storage import storage

router = APIRouter()


@router.post("", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """Execute code with optional input"""
    result = code_executor_service.execute_code(
        code=request.code,
        language=request.language,
        input_data=request.input,
    )
    
    return CodeExecutionResponse(
        success=result.success,
        output=result.output,
        error=result.error,
        execution_time=result.execution_time,
        memory_used=result.memory_used,
    )


@router.post("/test", response_model=SubmissionResponse)
async def execute_with_tests(request: TestExecutionRequest):
    """
    Execute code and run test cases
    Returns results for sample test cases, and optionally hidden test cases
    """
    try:
        # Get assessment first (this will auto-create default-assessment if needed)
        assessment = storage.get_assessment(request.assessment_id)
        if not assessment:
            # Try to auto-create default assessment
            if request.assessment_id == 'default-assessment':
                from app.db.seed_data import create_default_assessment
                assessment = create_default_assessment()
            else:
                raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Run test cases
        test_results, compilation_logs = code_executor_service.run_test_cases(
            code=request.code,
            language=request.language,
            question_id=request.question_id,
            include_hidden=request.include_hidden,
        )
        
        question = None
        for q in assessment.questions:
            if q.id == request.question_id:
                question = q
                break
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Create sets of test case IDs for quick lookup
        sample_test_case_ids = {tc.id for tc in question.sample_test_cases}
        hidden_test_case_ids = {tc.id for tc in question.hidden_test_cases}
        
        # Count passed test cases
        sample_passed = sum(
            1 for tr in test_results 
            if tr.passed and tr.test_case_id in sample_test_case_ids
        )
        sample_total = len(question.sample_test_cases)
        
        hidden_passed = sum(
            1 for tr in test_results 
            if tr.passed and tr.test_case_id in hidden_test_case_ids
        )
        hidden_total = len(question.hidden_test_cases) if request.include_hidden else 0
        
        # Create submission
        submission = Submission(
            id=str(uuid.uuid4()),
            assessment_id=request.assessment_id,
            question_id=request.question_id,
            candidate_id=request.candidate_id,
            code=request.code,
            language=request.language,
            test_results=test_results,
            sample_passed=sample_passed,
            sample_total=sample_total,
            hidden_passed=hidden_passed,
            hidden_total=hidden_total,
            compilation_logs=compilation_logs,
            submitted_at=datetime.utcnow(),
        )
        
        # Save submission
        saved_submission = storage.create_submission(submission)
        
        return saved_submission
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


@router.get("/submissions", response_model=list[SubmissionResponse])
async def get_submissions(
    assessment_id: Optional[str] = None,
    question_id: Optional[str] = None,
    candidate_id: Optional[str] = None,
):
    """Get submissions with optional filters"""
    submissions = storage.get_submissions(
        assessment_id=assessment_id,
        question_id=question_id,
        candidate_id=candidate_id,
    )
    return submissions

