"""Code execution endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.assessment import CodeExecutionRequest, CodeExecutionResponse
from app.services.code_executor import CodeExecutor
from app.core.config import settings

router = APIRouter()
executor = CodeExecutor()


@router.post("/run", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """Execute code without test cases (for testing/debugging)."""
    # Validate code length
    if len(request.code) > settings.MAX_CODE_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code exceeds maximum length of {settings.MAX_CODE_LENGTH} characters"
        )
    
    # Execute code
    result = await executor.execute_code(
        code=request.code,
        language=request.language,
        input_data=request.input_data
    )
    
    return CodeExecutionResponse(
        success=result.get("success", False),
        stdout=result.get("stdout", ""),
        stderr=result.get("stderr", ""),
        execution_time_ms=result.get("execution_time_ms", 0),
        return_code=result.get("return_code"),
        error=result.get("error"),
    )

