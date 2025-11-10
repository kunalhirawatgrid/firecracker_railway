"""
Helper functions for seeding default data
"""
from datetime import datetime
from app.models.assessment import Assessment, Question, TestCase, TestCaseType, Language
from app.db.json_storage import storage


def create_default_assessment():
    """Create default assessment for demo purposes"""
    # Check if already exists
    existing = storage.get_assessment('default-assessment')
    if existing:
        return existing
    
    sample_tcs = [
        TestCase(
            id='tc1',
            input='[2, 7, 11, 15]\n9',
            expected_output='[0, 1]',
            type=TestCaseType.SAMPLE,
            description='Basic test case',
        ),
        TestCase(
            id='tc2',
            input='[3, 2, 4]\n6',
            expected_output='[1, 2]',
            type=TestCaseType.SAMPLE,
            description='Different indices',
        ),
    ]
    
    hidden_tcs = [
        TestCase(
            id='tc3',
            input='[3, 3]\n6',
            expected_output='[0, 1]',
            type=TestCaseType.HIDDEN,
            description='Duplicate numbers',
        ),
    ]
    
    question = Question(
        id='q1',
        title='Two Sum',
        description='Given an array of integers and a target sum, find two numbers that add up to the target. Return the indices of the two numbers.',
        difficulty='easy',
        sample_test_cases=sample_tcs,
        hidden_test_cases=hidden_tcs,
        allowed_languages=[Language.PYTHON, Language.JAVA, Language.CPP, Language.JAVASCRIPT],
        time_limit=30,
    )
    
    assessment = Assessment(
        id='default-assessment',
        title='Sample Coding Assessment',
        description='This is a sample assessment to demonstrate the platform',
        questions=[question],
        duration=60,
        created_at=datetime.utcnow(),
    )
    
    return storage.create_assessment(assessment)

