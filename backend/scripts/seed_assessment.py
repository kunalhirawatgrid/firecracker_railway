#!/usr/bin/env python3
"""
Seed script to create a default assessment for testing
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.json_storage import storage
from app.models.assessment import Assessment, Question, TestCase, TestCaseType, Language
from datetime import datetime

def create_default_assessment():
    """Create a default assessment for testing"""
    
    # Check if assessment already exists
    existing = storage.get_assessment('default-assessment')
    if existing:
        print("Default assessment already exists!")
        return existing
    
    # Create test cases
    sample_test_cases = [
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
    
    hidden_test_cases = [
        TestCase(
            id='tc3',
            input='[3, 3]\n6',
            expected_output='[0, 1]',
            type=TestCaseType.HIDDEN,
            description='Duplicate numbers',
        ),
    ]
    
    # Create question
    question = Question(
        id='q1',
        title='Two Sum',
        description='Given an array of integers and a target sum, find two numbers that add up to the target. Return the indices of the two numbers.',
        difficulty='easy',
        sample_test_cases=sample_test_cases,
        hidden_test_cases=hidden_test_cases,
        allowed_languages=[Language.PYTHON, Language.JAVA, Language.CPP, Language.JAVASCRIPT],
        time_limit=30,
    )
    
    # Create assessment
    assessment = Assessment(
        id='default-assessment',
        title='Sample Coding Assessment',
        description='This is a sample assessment to demonstrate the platform',
        questions=[question],
        duration=60,
        created_at=datetime.utcnow(),
    )
    
    # Save assessment
    created = storage.create_assessment(assessment)
    print(f"✓ Created default assessment: {created.id}")
    print(f"  Title: {created.title}")
    print(f"  Questions: {len(created.questions)}")
    return created

if __name__ == '__main__':
    create_default_assessment()

