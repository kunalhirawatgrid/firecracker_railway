"""
Script to seed initial assessment data for testing.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.json_storage import storage
from datetime import datetime


def seed_assessment():
    """Create a sample assessment with questions and test cases."""
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    # storage.clear()
    
    # Create assessment
    assessment_data = {
        "title": "Python Coding Assessment",
        "description": "Test your Python programming skills with these coding challenges.",
        "duration_minutes": 60,
        "candidate_id": "candidate_1",
        "status": "not_started",
    }
    assessment = storage.create("assessments", assessment_data)
    assessment_id = assessment["id"]
    
    print(f"Created assessment with ID: {assessment_id}")
    
    # Question 1: Two Sum
    question1_data = {
        "assessment_id": assessment_id,
        "title": "Two Sum",
        "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Your code should read input in the format:
First line: space-separated integers (the array)
Second line: target integer

Output: [index1, index2] as a list""",
        "difficulty": "easy",
        "order": 1,
    }
    question1 = storage.create("questions", question1_data)
    question1_id = question1["id"]
    
    # Test cases for Question 1
    test_cases_q1 = [
        {
            "question_id": question1_id,
            "input_data": "2 7 11 15\n9",
            "expected_output": "[0, 1]",
            "is_sample": True,
            "order": 1,
        },
        {
            "question_id": question1_id,
            "input_data": "3 2 4\n6",
            "expected_output": "[1, 2]",
            "is_sample": True,
            "order": 2,
        },
        {
            "question_id": question1_id,
            "input_data": "3 3\n6",
            "expected_output": "[0, 1]",
            "is_sample": False,
            "order": 3,
        },
    ]
    
    for tc in test_cases_q1:
        storage.create("test_cases", tc)
    
    print(f"Created question 1: Two Sum (ID: {question1_id})")
    
    # Question 2: Reverse String
    question2_data = {
        "assessment_id": assessment_id,
        "title": "Reverse String",
        "description": """Write a function that reverses a string. The input string is given as an array of characters.

You must do this by modifying the input array in-place with O(1) extra memory.

Example:
Input: ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]

Your code should read input as a single line string and output the reversed string.

Example:
Input: hello
Output: olleh""",
        "difficulty": "easy",
        "order": 2,
    }
    question2 = storage.create("questions", question2_data)
    question2_id = question2["id"]
    
    # Test cases for Question 2
    test_cases_q2 = [
        {
            "question_id": question2_id,
            "input_data": "hello",
            "expected_output": "olleh",
            "is_sample": True,
            "order": 1,
        },
        {
            "question_id": question2_id,
            "input_data": "Python",
            "expected_output": "nohtyP",
            "is_sample": True,
            "order": 2,
        },
        {
            "question_id": question2_id,
            "input_data": "racecar",
            "expected_output": "racecar",
            "is_sample": False,
            "order": 3,
        },
    ]
    
    for tc in test_cases_q2:
        storage.create("test_cases", tc)
    
    print(f"Created question 2: Reverse String (ID: {question2_id})")
    
    # Question 3: Fibonacci
    question3_data = {
        "assessment_id": assessment_id,
        "title": "Fibonacci Number",
        "description": """The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1. That is,

F(0) = 0, F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1.

Given n, calculate F(n).

Example:
Input: n = 2
Output: 1
Explanation: F(2) = F(1) + F(0) = 1 + 0 = 1.

Your code should read a single integer n and output F(n).

Example:
Input: 5
Output: 5""",
        "difficulty": "easy",
        "order": 3,
    }
    question3 = storage.create("questions", question3_data)
    question3_id = question3["id"]
    
    # Test cases for Question 3
    test_cases_q3 = [
        {
            "question_id": question3_id,
            "input_data": "2",
            "expected_output": "1",
            "is_sample": True,
            "order": 1,
        },
        {
            "question_id": question3_id,
            "input_data": "5",
            "expected_output": "5",
            "is_sample": True,
            "order": 2,
        },
        {
            "question_id": question3_id,
            "input_data": "10",
            "expected_output": "55",
            "is_sample": False,
            "order": 3,
        },
    ]
    
    for tc in test_cases_q3:
        storage.create("test_cases", tc)
    
    print(f"Created question 3: Fibonacci Number (ID: {question3_id})")
    
    print(f"\n✅ Successfully created assessment with ID: {assessment_id}")
    print(f"   Access it at: http://localhost:5173/assessment/{assessment_id}?candidate_id=candidate_1")
    print(f"\n   Or use the API: http://localhost:8000/api/v1/assessments/{assessment_id}?candidate_id=candidate_1")


if __name__ == "__main__":
    seed_assessment()

