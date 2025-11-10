import subprocess
import tempfile
import os
import time
import shutil
from pathlib import Path
from typing import Optional, Tuple
from app.models.assessment import Language, ExecutionResult
from app.core.config import settings


class GVisorExecutor:
    """Execute code in gVisor sandbox using Docker with runsc runtime"""
    
    def __init__(self):
        self.runtime_path = settings.gvisor_runtime_path
        self.timeout = settings.gvisor_timeout
        self.memory_limit = settings.gvisor_memory_limit
        self.cpu_limit = settings.gvisor_cpu_limit
        self._gvisor_available = None  # Cache for availability check
    
    def _check_gvisor_available(self) -> bool:
        """Check if gVisor runtime is available in Docker"""
        if self._gvisor_available is not None:
            return self._gvisor_available
        
        try:
            # Check if runsc is available
            result = subprocess.run(
                ["docker", "info", "--format", "{{.Runtimes}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and "runsc" in result.stdout:
                self._gvisor_available = True
                return True
            
            # Try to verify runsc binary exists
            if os.path.exists(self.runtime_path):
                # Try a test run
                test_result = subprocess.run(
                    ["docker", "run", "--runtime", "runsc", "--rm", "hello-world"],
                    capture_output=True,
                    timeout=10,
                )
                if test_result.returncode == 0:
                    self._gvisor_available = True
                    return True
            
            self._gvisor_available = False
            return False
        except Exception:
            self._gvisor_available = False
            return False
    
    def _get_dockerfile(self, language: Language, code_file: str) -> str:
        """Generate Dockerfile based on language"""
        if language == Language.PYTHON:
            return f"""
FROM python:3.11-slim
WORKDIR /app
COPY {code_file} solution.py
CMD ["python", "solution.py"]
"""
        elif language == Language.JAVA:
            return f"""
FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app
COPY {code_file} Solution.java
RUN javac Solution.java
CMD ["java", "Solution"]
"""
        elif language == Language.CPP:
            return f"""
FROM gcc:12
WORKDIR /app
COPY {code_file} solution.cpp
RUN g++ -std=c++17 -O2 -o solution solution.cpp
CMD ["./solution"]
"""
        elif language == Language.JAVASCRIPT:
            return f"""
FROM node:18-slim
WORKDIR /app
COPY {code_file} solution.js
CMD ["node", "solution.js"]
"""
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _get_code_filename(self, language: Language) -> str:
        """Get the code filename for the given language"""
        extensions = {
            Language.PYTHON: "solution.py",
            Language.JAVA: "Solution.java",
            Language.CPP: "solution.cpp",
            Language.JAVASCRIPT: "solution.js",
        }
        return extensions[language]
    
    def _run_in_gvisor(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> Tuple[str, str, Optional[float], Optional[int]]:
        """
        Execute code in gVisor sandbox
        Returns: (stdout, stderr, execution_time, memory_used)
        """
        # Normalize input_data to string if it's not None
        if input_data is not None and not isinstance(input_data, str):
            if isinstance(input_data, bytes):
                input_data = input_data.decode('utf-8')
            else:
                input_data = str(input_data)
        
        # Check if gVisor is available
        use_gvisor = self._check_gvisor_available()
        if not use_gvisor:
            if settings.gvisor_fallback_to_docker:
                # Fallback to regular Docker (less secure, for development only)
                use_gvisor = False
            else:
                error_msg = (
                    "gVisor runtime (runsc) is not available. "
                    "Please install and configure gVisor:\n"
                    "1. Install gVisor: curl -fsSL https://gvisor.dev/install | bash\n"
                    "2. Configure Docker: Add 'runsc' runtime to /etc/docker/daemon.json\n"
                    "   Example: {\"runtimes\": {\"runsc\": {\"path\": \"/usr/local/bin/runsc\"}}}\n"
                    "3. Restart Docker: sudo systemctl restart docker\n"
                    "4. Verify: docker run --runtime=runsc hello-world\n\n"
                    "Alternatively, set GVISOR_FALLBACK_TO_DOCKER=true for development (less secure)"
                )
                return "", error_msg, None, None
        
        temp_dir = tempfile.mkdtemp(prefix="gvisor_exec_")
        try:
            # Write code to a file
            code_filename = self._get_code_filename(language)
            code_file_path = Path(temp_dir) / code_filename
            code_file_path.write_text(code, encoding='utf-8')
            
            # Create Dockerfile
            dockerfile_content = self._get_dockerfile(language, code_filename)
            dockerfile_path = Path(temp_dir) / "Dockerfile"
            dockerfile_path.write_text(dockerfile_content)
            
            # Build Docker image
            image_name = f"gvisor-exec-{int(time.time())}"
            build_cmd = [
                "docker", "build",
                "-t", image_name,
                "-f", str(dockerfile_path),
                temp_dir,
            ]
            
            # Use longer timeout for build (especially C++ compilation)
            build_timeout = self.timeout * 2  # Double timeout for builds
            build_result = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                timeout=build_timeout,
            )
            
            if build_result.returncode != 0:
                return "", build_result.stderr, None, None
            
            # Run container with gVisor runtime (or fallback to regular Docker)
            run_cmd = [
                "docker", "run",
                "--rm",
                "--memory", self.memory_limit,
                "--cpus", self.cpu_limit,
                "--network", "none",  # Disable network for security
                "--read-only",  # Read-only filesystem
            ]
            
            if use_gvisor:
                run_cmd.extend(["--runtime", "runsc"])  # Use gVisor runtime
            
            run_cmd.append(image_name)
            
            start_time = time.time()
            # Prepare input data - when text=True, subprocess expects a string, not bytes
            # Normalize input_data to string if provided
            input_str = None
            if input_data is not None:
                if isinstance(input_data, bytes):
                    input_str = input_data.decode('utf-8')
                elif isinstance(input_data, str):
                    input_str = input_data
                else:
                    input_str = str(input_data)
            
            run_result = subprocess.run(
                run_cmd,
                input=input_str,  # Pass string when text=True
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            execution_time = time.time() - start_time
            
            # Cleanup image
            try:
                subprocess.run(
                    ["docker", "rmi", image_name],
                    capture_output=True,
                    timeout=5,
                )
            except:
                pass
            
            return (
                run_result.stdout,
                run_result.stderr,
                execution_time,
                None,  # Memory usage would require additional monitoring
            )
        
        except subprocess.TimeoutExpired:
            return "", f"Execution timeout after {self.timeout} seconds", None, None
        except Exception as e:
            import traceback
            error_msg = f"{type(e).__name__}: {str(e)}"
            # Include traceback in error for debugging
            traceback_str = traceback.format_exc()
            return "", f"{error_msg}\n{traceback_str}", None, None
        finally:
            # Cleanup temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def execute(
        self,
        code: str,
        language: Language,
        input_data: Optional[str] = None,
    ) -> ExecutionResult:
        """
        Execute code and return result
        """
        stdout, stderr, exec_time, memory = self._run_in_gvisor(code, language, input_data)
        
        # Combine stdout and stderr for error detection
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
            memory_used=memory,
        )
    
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
executor = GVisorExecutor()

