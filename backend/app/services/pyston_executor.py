"""
Pyston executor using aiopyston library
Uses Piston API for secure code execution
"""
import asyncio
import concurrent.futures
from typing import Optional, Tuple
from pyston import PystonClient, File
from app.models.assessment import Language, ExecutionResult
from app.core.config import settings


class PystonExecutor:
    """Execute code using Pyston API (Piston API wrapper)"""
    
    def __init__(self):
        self.timeout = settings.gvisor_timeout
    
    async def _get_client(self):
        """Create a new PystonClient for each execution (required for concurrent executions)"""
        # Create a new client for each execution since each execution may run in a different event loop
        # This is necessary when running multiple test cases concurrently
        return PystonClient()
    
    def _map_language(self, language: Language) -> str:
        """Map our Language enum to Pyston API language identifiers"""
        mapping = {
            Language.PYTHON: "python",
            Language.JAVA: "java",
            Language.CPP: "cpp",
            Language.JAVASCRIPT: "javascript",
        }
        return mapping.get(language, "python")
    
    async def _execute_async(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> Tuple[str, str, Optional[float]]:
        """
        Execute code asynchronously using Pyston API
        Returns: (stdout, stderr, execution_time)
        """
        client = None
        try:
            lang = self._map_language(language)
            
            # Create a new client for this execution (each execution may be in a different event loop)
            client = await self._get_client()
            
            # Create file with code
            code_file = File(code)
            
            # Execute with timeout
            import time
            start_time = time.time()
            
            # Use asyncio.wait_for for timeout handling
            # Piston API v2 execute signature: execute(language, files, stdin=None)
            execute_kwargs = {"stdin": input_data} if input_data else {}
            output = await asyncio.wait_for(
                client.execute(lang, [code_file], **execute_kwargs),
                timeout=self.timeout
            )
            
            execution_time = time.time() - start_time
            
            # Extract output and error from Pyston response
            stdout = ""
            stderr = ""
            
            if output:
                # Pyston Output object structure (based on Piston API v2)
                # Output has 'run' and 'compile' stages
                if hasattr(output, 'run') and output.run:
                    # Run stage contains stdout and stderr
                    if hasattr(output.run, 'stdout'):
                        stdout = output.run.stdout or ""
                    if hasattr(output.run, 'stderr'):
                        stderr = output.run.stderr or ""
                
                # Check compile stage for errors
                if hasattr(output, 'compile') and output.compile:
                    if hasattr(output.compile, 'stderr') and output.compile.stderr:
                        # Prepend compilation errors
                        stderr = (output.compile.stderr + "\n" + stderr).strip()
                
                # Fallback: check for direct stdout/stderr attributes
                if not stdout and hasattr(output, 'stdout'):
                    stdout = output.stdout or ""
                if not stderr and hasattr(output, 'stderr'):
                    stderr = output.stderr or ""
                
                # Last resort: if output is a string
                if not stdout and not stderr:
                    stdout = str(output) if output else ""
            
            return stdout, stderr, execution_time
            
        except asyncio.TimeoutError:
            return "", f"Execution timeout after {self.timeout} seconds", None
        except Exception as e:
            import traceback
            error_msg = f"{type(e).__name__}: {str(e)}"
            traceback_str = traceback.format_exc()
            return "", f"{error_msg}\n{traceback_str}", None
        finally:
            # Clean up client session if it exists
            if client is not None:
                try:
                    await client.close_session()
                except Exception:
                    # Ignore errors during cleanup
                    pass
    
    def execute(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> ExecutionResult:
        """
        Execute code and return result (synchronous wrapper)
        Works both in sync and async contexts
        """
        # Check if we're in an async context with a running event loop
        try:
            loop = asyncio.get_running_loop()
            # We're in an async context - run in a thread pool to avoid nested event loop
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self._run_in_new_loop, code, language, input_data)
                stdout, stderr, exec_time = future.result()
        except RuntimeError:
            # No running loop - we can use asyncio.run()
            stdout, stderr, exec_time = self._run_in_new_loop(code, language, input_data)
        
        # Determine success
        error = stderr if stderr and stderr.strip() else None
        success = error is None or (not error.strip())
        
        # If there's stderr but no stdout, treat as error
        if stderr and stderr.strip() and not stdout:
            error = stderr
            success = False
        
        return ExecutionResult(
            success=success,
            output=stdout.strip() if stdout else "",
            error=error,
            execution_time=exec_time,
            memory_used=None,  # Pyston API doesn't provide memory usage
        )
    
    def _run_in_new_loop(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> Tuple[str, str, Optional[float]]:
        """Run async execution in a new event loop"""
        return asyncio.run(self._execute_async(code, language, input_data))
    
    def execute_with_test_case(
        self,
        code: str,
        language: Language,
        input_data: str,
        expected_output: str,
    ) -> Tuple[bool, str, Optional[str], Optional[float]]:
        """
        Execute code with test case and compare output
        Returns: (passed, actual_output, error, execution_time)
        """
        result = self.execute(code, language, input_data)
        
        if not result.success:
            return False, "", result.error, result.execution_time
        
        # Normalize outputs for comparison
        actual = result.output.strip()
        expected = expected_output.strip()
        
        passed = actual == expected
        return passed, actual, result.error, result.execution_time


# Global executor instance
executor = PystonExecutor()

