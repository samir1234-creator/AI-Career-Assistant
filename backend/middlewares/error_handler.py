from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.exceptions import AppException
from core.response import BaseResponse

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(success=False, message=exc.message).model_dump()
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponse(success=False, message="An unexpected error occurred.").model_dump()
    )
