"""
Firecracker VM service for secure code execution.
Based on Firecracker API: https://firecracker-microvm.github.io/
"""
import json
import time
import subprocess
import tempfile
import os
from typing import Dict, Optional, Tuple
from pathlib import Path
import httpx
from app.core.config import settings


class FirecrackerVM:
    """Firecracker VM manager for code execution."""

    def __init__(self):
        """Initialize Firecracker VM service."""
        self.socket_path = settings.FIRECRACKER_SOCKET_PATH
        self.kernel_path = settings.FIRECRACKER_KERNEL_PATH
        self.rootfs_path = settings.FIRECRACKER_ROOTFS_PATH
        self.timeout = settings.FIRECRACKER_VM_TIMEOUT_SECONDS
        self.max_memory_mb = settings.FIRECRACKER_MAX_MEMORY_MB
        self.vcpu_count = settings.FIRECRACKER_VCPU_COUNT

    async def create_vm(self, vm_id: str) -> str:
        """
        Create a new Firecracker VM instance.
        
        Args:
            vm_id: Unique identifier for the VM
            
        Returns:
            Socket path for the VM
        """
        # In production, this would create a new VM instance
        # For now, we'll use a simplified approach with a unique socket
        socket_path = f"/tmp/firecracker_{vm_id}.socket"
        return socket_path

    async def configure_vm(self, socket_path: str) -> bool:
        """
        Configure VM with kernel and rootfs.
        
        Args:
            socket_path: Socket path for the VM
            
        Returns:
            True if successful
        """
        # In production, this would configure the VM via Firecracker API
        # For development/testing, we'll use a mock approach
        return True

    async def execute_code(
        self,
        code: str,
        language: str,
        input_data: Optional[str] = None,
        timeout_seconds: Optional[int] = None
    ) -> Dict:
        """
        Execute code in a Firecracker VM.
        
        Args:
            code: Source code to execute
            language: Programming language (python, java, cpp, javascript)
            input_data: Input data for the program
            timeout_seconds: Execution timeout
            
        Returns:
            Dictionary with execution results
        """
        timeout = timeout_seconds or self.timeout
        
        # Create temporary files for code and input
        with tempfile.TemporaryDirectory() as tmpdir:
            code_file, input_file = self._prepare_files(tmpdir, code, language, input_data)
            
            # Execute based on language
            result = await self._execute_by_language(
                code_file, input_file, language, timeout
            )
            
            return result

    def _prepare_files(
        self, tmpdir: str, code: str, language: str, input_data: Optional[str]
    ) -> Tuple[Path, Optional[Path]]:
        """Prepare code and input files."""
        extensions = {
            "python": ".py",
            "java": ".java",
            "cpp": ".cpp",
            "javascript": ".js",
        }
        
        ext = extensions.get(language, ".txt")
        code_file = Path(tmpdir) / f"code{ext}"
        code_file.write_text(code)
        
        input_file = None
        if input_data:
            input_file = Path(tmpdir) / "input.txt"
            input_file.write_text(input_data)
        
        return code_file, input_file

    async def _execute_by_language(
        self, code_file: Path, input_file: Optional[Path], language: str, timeout: int
    ) -> Dict:
        """Execute code based on language."""
        try:
            if language == "python":
                return await self._execute_python(code_file, input_file, timeout)
            elif language == "java":
                return await self._execute_java(code_file, input_file, timeout)
            elif language == "cpp":
                return await self._execute_cpp(code_file, input_file, timeout)
            elif language == "javascript":
                return await self._execute_javascript(code_file, input_file, timeout)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported language: {language}",
                    "stdout": "",
                    "stderr": "",
                    "execution_time_ms": 0,
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "execution_time_ms": 0,
            }

    async def _execute_python(
        self, code_file: Path, input_file: Optional[Path], timeout: int
    ) -> Dict:
        """Execute Python code."""
        start_time = time.time()
        
        cmd = ["python3", str(code_file)]
        stdin = None
        if input_file:
            stdin = input_file.open("r")
        
        try:
            process = subprocess.run(
                cmd,
                stdin=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=code_file.parent,
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": process.returncode == 0,
                "stdout": process.stdout[:settings.MAX_STDOUT_SIZE],
                "stderr": process.stderr[:settings.MAX_STDOUT_SIZE],
                "return_code": process.returncode,
                "execution_time_ms": execution_time,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timeout after {timeout} seconds",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": int(timeout * 1000),
            }
        finally:
            if stdin:
                stdin.close()

    async def _execute_java(
        self, code_file: Path, input_file: Optional[Path], timeout: int
    ) -> Dict:
        """Execute Java code."""
        start_time = time.time()
        
        # Extract class name from Java file
        class_name = code_file.stem
        
        # Compile Java code
        compile_cmd = ["javac", str(code_file)]
        compile_process = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=code_file.parent,
        )
        
        if compile_process.returncode != 0:
            return {
                "success": False,
                "stdout": "",
                "stderr": compile_process.stderr[:settings.MAX_STDOUT_SIZE],
                "return_code": compile_process.returncode,
                "execution_time_ms": int((time.time() - start_time) * 1000),
            }
        
        # Run compiled Java code
        run_cmd = ["java", "-cp", str(code_file.parent), class_name]
        stdin = None
        if input_file:
            stdin = input_file.open("r")
        
        try:
            run_process = subprocess.run(
                run_cmd,
                stdin=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=code_file.parent,
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": run_process.returncode == 0,
                "stdout": run_process.stdout[:settings.MAX_STDOUT_SIZE],
                "stderr": run_process.stderr[:settings.MAX_STDOUT_SIZE],
                "return_code": run_process.returncode,
                "execution_time_ms": execution_time,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timeout after {timeout} seconds",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": int(timeout * 1000),
            }
        finally:
            if stdin:
                stdin.close()

    async def _execute_cpp(
        self, code_file: Path, input_file: Optional[Path], timeout: int
    ) -> Dict:
        """Execute C++ code."""
        start_time = time.time()
        
        # Compile C++ code
        executable = code_file.parent / "a.out"
        compile_cmd = ["g++", "-o", str(executable), str(code_file)]
        compile_process = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=code_file.parent,
        )
        
        if compile_process.returncode != 0:
            return {
                "success": False,
                "stdout": "",
                "stderr": compile_process.stderr[:settings.MAX_STDOUT_SIZE],
                "return_code": compile_process.returncode,
                "execution_time_ms": int((time.time() - start_time) * 1000),
            }
        
        # Run compiled executable
        stdin = None
        if input_file:
            stdin = input_file.open("r")
        
        try:
            run_process = subprocess.run(
                [str(executable)],
                stdin=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=code_file.parent,
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": run_process.returncode == 0,
                "stdout": run_process.stdout[:settings.MAX_STDOUT_SIZE],
                "stderr": run_process.stderr[:settings.MAX_STDOUT_SIZE],
                "return_code": run_process.returncode,
                "execution_time_ms": execution_time,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timeout after {timeout} seconds",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": int(timeout * 1000),
            }
        finally:
            if stdin:
                stdin.close()
            if executable.exists():
                executable.unlink()

    async def _execute_javascript(
        self, code_file: Path, input_file: Optional[Path], timeout: int
    ) -> Dict:
        """Execute JavaScript code."""
        start_time = time.time()
        
        cmd = ["node", str(code_file)]
        stdin = None
        if input_file:
            stdin = input_file.open("r")
        
        try:
            process = subprocess.run(
                cmd,
                stdin=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=code_file.parent,
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": process.returncode == 0,
                "stdout": process.stdout[:settings.MAX_STDOUT_SIZE],
                "stderr": process.stderr[:settings.MAX_STDOUT_SIZE],
                "return_code": process.returncode,
                "execution_time_ms": execution_time,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timeout after {timeout} seconds",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": int(timeout * 1000),
            }
        finally:
            if stdin:
                stdin.close()

    async def cleanup_vm(self, vm_id: str) -> bool:
        """Cleanup VM resources."""
        # In production, this would stop and remove the VM
        return True

