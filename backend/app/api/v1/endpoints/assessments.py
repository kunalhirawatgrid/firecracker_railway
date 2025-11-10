from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime
from app.schemas.assessment import AssessmentResponse, AssessmentCreate
from app.models.assessment import Assessment, Question, TestCase, TestCaseType, Language
from app.db.json_storage import storage
from app.db.seed_data import create_default_assessment

router = APIRouter()


@router.get("", response_model=List[AssessmentResponse])
async def get_assessments():
    """Get all assessments"""
    assessments = storage.get_all_assessments()
    return assessments


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: str):
    """Get assessment by ID"""
    assessment = storage.get_assessment(assessment_id)
    if not assessment:
        # Auto-create default assessment if requested
        if assessment_id == 'default-assessment':
            try:
                assessment = create_default_assessment()
            except Exception as e:
                # Log error and re-raise
                import logging
                logging.error(f"Error creating default assessment: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to create default assessment: {str(e)}")
        else:
            raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.post("/assessments", response_model=AssessmentResponse, status_code=201)
async def create_assessment(assessment_data: AssessmentCreate):
    """Create a new assessment"""
    # Convert question data to Question objects
    questions = []
    for q_data in assessment_data.questions:
        sample_tcs = [
            TestCase(
                id=tc.get("id", str(uuid.uuid4())),
                input=tc["input"],
                expected_output=tc["expected_output"],
                type=TestCaseType.SAMPLE,
                description=tc.get("description"),
            )
            for tc in q_data.get("sample_test_cases", [])
        ]
        hidden_tcs = [
            TestCase(
                id=tc.get("id", str(uuid.uuid4())),
                input=tc["input"],
                expected_output=tc["expected_output"],
                type=TestCaseType.HIDDEN,
                description=tc.get("description"),
            )
            for tc in q_data.get("hidden_test_cases", [])
        ]
        
        question = Question(
            id=q_data.get("id", str(uuid.uuid4())),
            title=q_data["title"],
            description=q_data["description"],
            difficulty=q_data.get("difficulty", "medium"),
            sample_test_cases=sample_tcs,
            hidden_test_cases=hidden_tcs,
            allowed_languages=[Language(lang) for lang in q_data.get("allowed_languages", ["python"])],
            time_limit=q_data.get("time_limit", 60),
        )
        questions.append(question)
    
    assessment = Assessment(
        id=str(uuid.uuid4()),
        title=assessment_data.title,
        description=assessment_data.description,
        questions=questions,
        duration=assessment_data.duration,
        created_at=datetime.utcnow(),
    )
    
    created_assessment = storage.create_assessment(assessment)
    return created_assessment

