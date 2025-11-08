"""Assessment endpoints."""
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.db.session import get_db, JSONSession
from app.models.json_models import (
    Assessment,
    Question,
    TestCase,
    Submission,
    TestResult,
    AssessmentStatus,
)
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentStart,
    QuestionResponse,
    SubmissionRequest,
    SubmissionResponse,
    TestCaseResponse,
)
from app.services.code_executor import CodeExecutor

router = APIRouter()


def _assessment_to_dict(assessment: Assessment) -> dict:
    """Convert Assessment to dict for response."""
    return {
        "id": assessment.id,
        "title": assessment.title,
        "description": assessment.description,
        "duration_minutes": assessment.duration_minutes,
        "candidate_id": assessment.candidate_id,
        "status": assessment.status,
        "started_at": assessment.started_at,
        "expires_at": assessment.expires_at,
        "created_at": assessment.created_at,
        "updated_at": assessment.updated_at,
    }


@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment: AssessmentCreate,
    db: JSONSession = Depends(get_db)
):
    """Create a new assessment."""
    # Create assessment
    assessment_dict = {
        "title": assessment.title,
        "description": assessment.description,
        "duration_minutes": assessment.duration_minutes,
        "candidate_id": assessment.candidate_id,
        "status": AssessmentStatus.NOT_STARTED.value,
    }
    db_assessment_data = db.storage.create("assessments", assessment_dict)
    db_assessment = Assessment.from_dict(db_assessment_data)
    
    # Add questions
    for q_order, question_data in enumerate(assessment.questions, start=1):
        question_dict = {
            "assessment_id": db_assessment.id,
            "title": question_data.title,
            "description": question_data.description,
            "difficulty": question_data.difficulty,
            "order": q_order,
            "time_limit_minutes": question_data.time_limit_minutes,
        }
        db_question_data = db.storage.create("questions", question_dict)
        db_question = Question.from_dict(db_question_data)
        
        # Add test cases
        for tc_order, test_case_data in enumerate(question_data.test_cases, start=1):
            test_case_dict = {
                "question_id": db_question.id,
                "input_data": test_case_data.input_data,
                "expected_output": test_case_data.expected_output,
                "is_sample": test_case_data.is_sample,
                "order": tc_order,
            }
            db.storage.create("test_cases", test_case_dict)
    
    return _assessment_to_dict(db_assessment)


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: int,
    candidate_id: str = Query(..., description="Candidate ID"),
    db: JSONSession = Depends(get_db)
):
    """Get assessment by ID."""
    assessment_data = db.storage.get("assessments", assessment_id)
    
    if not assessment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    assessment = Assessment.from_dict(assessment_data)
    
    if assessment.candidate_id != candidate_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Load questions (not needed for response, but available if needed)
    # Questions are loaded separately via the /questions endpoint
    
    return _assessment_to_dict(assessment)


@router.post("/{assessment_id}/start", response_model=AssessmentResponse)
async def start_assessment(
    assessment_id: int,
    start_data: AssessmentStart,
    db: JSONSession = Depends(get_db)
):
    """Start an assessment."""
    assessment_data = db.storage.get("assessments", assessment_id)
    
    if not assessment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    assessment = Assessment.from_dict(assessment_data)
    
    if assessment.candidate_id != start_data.candidate_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    if assessment.status != AssessmentStatus.NOT_STARTED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment already started or completed"
        )
    
    # Set start time and expiration
    started_at = datetime.utcnow()
    expires_at = started_at + timedelta(minutes=assessment.duration_minutes)
    
    updated_data = db.storage.update(
        "assessments",
        assessment_id,
        {
            "status": AssessmentStatus.IN_PROGRESS.value,
            "started_at": started_at.isoformat() + "Z",
            "expires_at": expires_at.isoformat() + "Z",
        }
    )
    
    return Assessment.from_dict(updated_data).to_dict()


@router.get("/{assessment_id}/questions", response_model=List[QuestionResponse])
async def get_questions(
    assessment_id: int,
    candidate_id: str = Query(..., description="Candidate ID"),
    db: JSONSession = Depends(get_db)
):
    """Get questions for an assessment."""
    assessment_data = db.storage.get("assessments", assessment_id)
    
    if not assessment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    assessment = Assessment.from_dict(assessment_data)
    
    if assessment.candidate_id != candidate_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    questions_data = db.storage.query("questions", assessment_id=assessment_id)
    questions = [Question.from_dict(q) for q in questions_data]
    questions.sort(key=lambda x: x.order)
    
    # Load test cases for each question
    result = []
    for question in questions:
        test_cases_data = db.storage.query("test_cases", question_id=question.id)
        test_cases = [TestCase.from_dict(tc) for tc in test_cases_data]
        test_cases.sort(key=lambda x: x.order)
        
        question_dict = question.to_dict()
        question_dict["test_cases"] = [
            {
                "id": tc.id,
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_sample": tc.is_sample,
                "order": tc.order,
            }
            for tc in test_cases
        ]
        result.append(question_dict)
    
    return result


@router.post("/{assessment_id}/questions/{question_id}/submit", response_model=SubmissionResponse)
async def submit_solution(
    assessment_id: int,
    question_id: int,
    submission: SubmissionRequest,
    candidate_id: str = Query(..., description="Candidate ID"),
    db: JSONSession = Depends(get_db)
):
    """Submit a solution for a question."""
    # Verify assessment
    assessment_data = db.storage.get("assessments", assessment_id)
    
    if not assessment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    assessment = Assessment.from_dict(assessment_data)
    
    if assessment.candidate_id != candidate_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Check if assessment is still active
    if assessment.status != AssessmentStatus.IN_PROGRESS.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment is not in progress"
        )
    
    if assessment.expires_at:
        expires_at = datetime.fromisoformat(assessment.expires_at.replace("Z", "+00:00"))
        if datetime.utcnow() > expires_at:
            db.storage.update("assessments", assessment_id, {"status": AssessmentStatus.EXPIRED.value})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assessment has expired"
            )
    
    # Verify question belongs to assessment
    question_data = db.storage.get("questions", question_id)
    
    if not question_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    question = Question.from_dict(question_data)
    
    if question.assessment_id != assessment_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Get test cases
    test_cases_data = db.storage.query("test_cases", question_id=question_id)
    test_cases = [TestCase.from_dict(tc) for tc in test_cases_data]
    test_cases.sort(key=lambda x: x.order)
    
    if not test_cases:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No test cases found for this question"
        )
    
    # Create submission
    submission_dict = {
        "assessment_id": assessment_id,
        "question_id": question_id,
        "candidate_id": candidate_id,
        "language": submission.language,
        "code": submission.code,
        "status": "running",
        "total_test_cases": len(test_cases),
    }
    db_submission_data = db.storage.create("submissions", submission_dict)
    db_submission = Submission.from_dict(db_submission_data)
    
    # Execute code
    executor = CodeExecutor()
    execution_result = await executor.run_tests(
        code=submission.code,
        language=submission.language,
        test_cases=test_cases,
        submission_id=db_submission.id,
        db=db,
        show_hidden=False  # Only show sample test cases to candidate
    )
    
    # Update submission
    updated_submission_data = db.storage.update(
        "submissions",
        db_submission.id,
        {
            "status": "completed",
            "passed_test_cases": execution_result["passed"],
            "compilation_logs": execution_result.get("compilation_logs", ""),
            "execution_logs": execution_result.get("execution_logs", ""),
            "execution_time_ms": execution_result["results"][0].get("execution_time_ms", 0) if execution_result["results"] else 0,
        }
    )
    
    # Get test results
    test_results_data = db.storage.query("test_results", submission_id=db_submission.id)
    test_results = [TestResult.from_dict(tr) for tr in test_results_data]
    
    # Get test case details for response
    test_case_map = {tc.id: tc for tc in test_cases}
    
    return {
        "id": updated_submission_data["id"],
        "question_id": updated_submission_data["question_id"],
        "language": updated_submission_data["language"],
        "status": updated_submission_data["status"],
        "passed_test_cases": updated_submission_data["passed_test_cases"],
        "total_test_cases": updated_submission_data["total_test_cases"],
        "compilation_logs": updated_submission_data["compilation_logs"],
        "execution_logs": updated_submission_data["execution_logs"],
        "execution_time_ms": updated_submission_data["execution_time_ms"],
        "test_results": [
            {
                "test_case_id": tr.test_case_id,
                "is_sample": test_case_map[tr.test_case_id].is_sample,
                "passed": tr.passed,
                "actual_output": tr.actual_output,
                "expected_output": test_case_map[tr.test_case_id].expected_output if test_case_map[tr.test_case_id].is_sample else None,
                "error": tr.error_message,
                "execution_time_ms": tr.execution_time_ms,
            }
            for tr in test_results
        ],
        "created_at": updated_submission_data["created_at"],
    }
