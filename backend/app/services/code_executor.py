from typing import List, Tuple, Optional
from app.models.assessment import (
    Language,
    TestCase,
    TestCaseType,
    TestResult,
    ExecutionResult,
)
from app.services.gvisor_executor import executor
from app.db.json_storage import storage
from app.models.assessment import Question


class CodeExecutorService:
    """Service for executing code and running test cases"""
    
    def execute_code(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute code with optional input"""
        return executor.execute(code, language, input_data)
    
    def run_test_cases(
        self,
        code: str,
        language: Language,
        question_id: str,
        include_hidden: bool = False,
    ) -> Tuple[List[TestResult], str]:
        """
        Run test cases for a question
        Returns: (test_results, compilation_logs)
        """
        # Get question from storage
        assessments = storage.get_all_assessments()
        question = None
        for assessment in assessments:
            for q in assessment.questions:
                if q.id == question_id:
                    question = q
                    break
            if question:
                break
        
        if not question:
            raise ValueError(f"Question {question_id} not found")
        
        # Check if language is allowed
        if language not in question.allowed_languages:
            raise ValueError(f"Language {language.value} not allowed for this question")
        
        test_results = []
        compilation_logs = ""
        
        # Run sample test cases
        for test_case in question.sample_test_cases:
            passed, actual_output, error, exec_time = executor.execute_with_test_case(
                code=code,
                language=language,
                input_data=test_case.input,
                expected_output=test_case.expected_output,
            )
            
            # Collect compilation errors
            if error and "error" in error.lower():
                compilation_logs += f"Test {test_case.id}: {error}\n"
            
            test_result = TestResult(
                test_case_id=test_case.id,
                passed=passed,
                input=test_case.input,
                expected_output=test_case.expected_output,
                actual_output=actual_output,
                error=error,
                execution_time=exec_time,
            )
            test_results.append(test_result)
        
        # Run hidden test cases if requested
        if include_hidden:
            for test_case in question.hidden_test_cases:
                passed, actual_output, error, exec_time = executor.execute_with_test_case(
                    code=code,
                    language=language,
                    input_data=test_case.input,
                    expected_output=test_case.expected_output,
                )
                
                if error and "error" in error.lower():
                    compilation_logs += f"Test {test_case.id}: {error}\n"
                
                test_result = TestResult(
                    test_case_id=test_case.id,
                    passed=passed,
                    input=test_case.input,
                    expected_output=test_case.expected_output,
                    actual_output=actual_output,
                    error=error,
                    execution_time=exec_time,
                )
                test_results.append(test_result)
        
        return test_results, compilation_logs.strip()


# Global service instance
code_executor_service = CodeExecutorService()

