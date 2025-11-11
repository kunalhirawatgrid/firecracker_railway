"""
Direct code executor using subprocess with resource limits
Used as fallback when Docker/gVisor is not available (e.g., Railway)
"""
import subprocess
import tempfile
import os
import time
import shutil
import resource
from pathlib import Path
from typing import Optional, Tuple
from app.models.assessment import Language, ExecutionResult
from app.core.config import settings


class DirectExecutor:
    """Execute code directly using subprocess with resource limits"""
    
    def __init__(self):
        self.timeout = settings.gvisor_timeout
        self.memory_limit_mb = self._parse_memory_limit(settings.gvisor_memory_limit)
        self.cpu_limit = float(settings.gvisor_cpu_limit)
    
    def _parse_memory_limit(self, limit_str: str) -> int:
        """Parse memory limit string (e.g., '512m') to MB"""
        limit_str = limit_str.lower().strip()
        if limit_str.endswith('m'):
            return int(limit_str[:-1])
        elif limit_str.endswith('g'):
            return int(limit_str[:-1]) * 1024
        elif limit_str.endswith('k'):
            return int(limit_str[:-1]) // 1024
        else:
            return int(limit_str)  # Assume MB
    
    def _set_resource_limits(self):
        """Set resource limits for the current process"""
        try:
            # Set memory limit (RSS - Resident Set Size)
            if self.memory_limit_mb:
                memory_bytes = self.memory_limit_mb * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
            
            # Set CPU time limit (soft and hard)
            # Note: This is a per-process limit, not per-thread
            cpu_seconds = int(self.timeout * self.cpu_limit)
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
        except (ValueError, OSError) as e:
            # Resource limits might not be available on all systems
            print(f"Warning: Could not set resource limits: {e}")
    
    def _get_code_file_extension(self, language: Language) -> str:
        """Get file extension for the given language"""
        extensions = {
            Language.PYTHON: ".py",
            Language.JAVA: ".java",
            Language.CPP: ".cpp",
            Language.JAVASCRIPT: ".js",
        }
        return extensions[language]
    
    def _get_execution_command(self, language: Language, code_file: Path) -> list:
        """Get the command to execute code for the given language"""
        if language == Language.PYTHON:
            return ["python3", str(code_file)]
        elif language == Language.JAVA:
            # Compile first, then run
            class_dir = code_file.parent
            class_name = code_file.stem
            compile_cmd = ["javac", str(code_file)]
            run_cmd = ["java", "-cp", str(class_dir), class_name]
            return {"compile": compile_cmd, "run": run_cmd}
        elif language == Language.CPP:
            # Compile first, then run
            exe_file = code_file.parent / "solution"
            compile_cmd = ["g++", "-std=c++17", "-O2", "-o", str(exe_file), str(code_file)]
            run_cmd = [str(exe_file)]
            return {"compile": compile_cmd, "run": run_cmd}
        elif language == Language.JAVASCRIPT:
            return ["node", str(code_file)]
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _run_with_limits(
        self,
        cmd: list,
        input_data: Optional[str] = None,
        cwd: Optional[Path] = None,
    ) -> Tuple[str, str, float]:
        """Run command with resource limits"""
        start_time = time.time()
        
        try:
            # Use prlimit if available (Linux) for better control
            preexec_fn = None
            if os.name == 'posix':
                try:
                    import prlimit
                    def set_limits():
                        if self.memory_limit_mb:
                            memory_bytes = self.memory_limit_mb * 1024 * 1024
                            prlimit.setrlimit(0, prlimit.RLIMIT_AS, (memory_bytes, memory_bytes))
                    preexec_fn = set_limits
                except ImportError:
                    # Fall back to resource module
                    preexec_fn = self._set_resource_limits
            
            result = subprocess.run(
                cmd,
                input=input_data.encode('utf-8') if input_data else None,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(cwd) if cwd else None,
                preexec_fn=preexec_fn,
            )
            
            execution_time = time.time() - start_time
            return result.stdout, result.stderr, execution_time
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return "", f"Execution timeout after {self.timeout} seconds", execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            return "", str(e), execution_time
    
    def execute(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> ExecutionResult:
        """
        Execute code directly using subprocess
        """
        temp_dir = tempfile.mkdtemp(prefix="direct_exec_")
        try:
            # Write code to a file
            ext = self._get_code_file_extension(language)
            code_file = Path(temp_dir) / f"solution{ext}"
            code_file.write_text(code, encoding='utf-8')
            
            # Get execution command
            cmd_info = self._get_execution_command(language, code_file)
            
            # Handle languages that need compilation
            if isinstance(cmd_info, dict):
                # Compile first
                compile_stdout, compile_stderr, compile_time = self._run_with_limits(
                    cmd_info["compile"],
                    cwd=temp_dir,
                )
                
                if compile_stderr:
                    # Compilation error
                    return ExecutionResult(
                        success=False,
                        output="",
                        error=compile_stderr,
                        execution_time=compile_time,
                    )
                
                # Run the compiled code
                stdout, stderr, exec_time = self._run_with_limits(
                    cmd_info["run"],
                    input_data=input_data,
                    cwd=temp_dir,
                )
                total_time = compile_time + exec_time
            else:
                # Direct execution (Python, JavaScript)
                stdout, stderr, exec_time = self._run_with_limits(
                    cmd_info,
                    input_data=input_data,
                    cwd=temp_dir,
                )
                total_time = exec_time
            
            # Determine success
            error = stderr if stderr and stderr.strip() else None
            success = error is None or (not error.strip())
            
            if stderr and stderr.strip() and not stdout:
                error = stderr
                success = False
            
            return ExecutionResult(
                success=success,
                output=stdout.strip() if stdout else "",
                error=error,
                execution_time=total_time,
                memory_used=None,  # Memory monitoring not available
            )
        
        except Exception as e:
            import traceback
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}\n{traceback.format_exc()}",
                execution_time=None,
            )
        finally:
            # Cleanup temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
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
direct_executor = DirectExecutor()

