"""
Code execution service that uses Firecracker VM.
"""
from typing import Dict, List, Optional
from app.services.firecracker import FirecrackerVM
from app.models.json_models import TestCase, TestResult
from app.db.session import JSONSession


class CodeExecutor:
    """Code execution service."""

    def __init__(self):
        """Initialize code executor."""
        self.vm = FirecrackerVM()

    async def run_tests(
        self,
        code: str,
        language: str,
        test_cases: List[TestCase],
        submission_id: int,
        db: JSONSession,
        show_hidden: bool = False
    ) -> Dict:
        """
        Run code against test cases.
        
        Args:
            code: Source code to test
            language: Programming language
            test_cases: List of test cases to run
            submission_id: Submission ID
            db: Database session
            show_hidden: Whether to show hidden test case results
            
        Returns:
            Dictionary with test results
        """
        # Filter test cases based on visibility
        visible_cases = [tc for tc in test_cases if tc.is_sample or show_hidden]
        
        results = []
        passed_count = 0
        total_count = len(visible_cases)
        
        for test_case in visible_cases:
            # Execute code with test case input
            execution_result = await self.vm.execute_code(
                code=code,
                language=language,
                input_data=test_case.input_data,
                timeout_seconds=10
            )
            
            # Compare output
            actual_output = execution_result.get("stdout", "").strip()
            expected_output = test_case.expected_output.strip()
            passed = actual_output == expected_output
            
            if passed:
                passed_count += 1
            
            # Create test result record
            error_message = execution_result.get("stderr") if not execution_result.get("success") else None
            execution_time = execution_result.get("execution_time_ms", 0)
            
            test_result_dict = {
                "submission_id": submission_id,
                "test_case_id": test_case.id,
                "passed": passed,
                "actual_output": actual_output if (test_case.is_sample or show_hidden) else None,
                "error_message": error_message,
                "execution_time_ms": execution_time,
            }
            db.storage.create("test_results", test_result_dict)
            
            results.append({
                "test_case_id": test_case.id,
                "is_sample": test_case.is_sample,
                "passed": passed,
                "actual_output": actual_output if (test_case.is_sample or show_hidden) else None,
                "expected_output": expected_output if test_case.is_sample else None,
                "error": error_message,
                "execution_time_ms": execution_time,
            })
        
        # Collect compilation and execution logs from all test runs
        all_stderr = []
        all_stdout = []
        
        # Get logs from the last execution (most recent)
        if execution_result:
            if execution_result.get("stderr"):
                all_stderr.append(execution_result.get("stderr"))
            if execution_result.get("stdout"):
                all_stdout.append(execution_result.get("stdout"))
        
        compilation_logs = "\n".join(all_stderr) if all_stderr else ""
        execution_logs = "\n".join(all_stdout) if all_stdout else ""
        
        return {
            "passed": passed_count,
            "total": total_count,
            "results": results,
            "compilation_logs": compilation_logs,
            "execution_logs": execution_logs,
        }

    async def execute_code(
        self,
        code: str,
        language: str,
        input_data: Optional[str] = None
    ) -> Dict:
        """
        Execute code and return results.
        
        Args:
            code: Source code
            language: Programming language
            input_data: Optional input data
            
        Returns:
            Execution results
        """
        return await self.vm.execute_code(
            code=code,
            language=language,
            input_data=input_data
        )

