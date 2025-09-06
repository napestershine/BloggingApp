"""
Comprehensive error handling middleware for consistent API responses
"""
import logging
from typing import Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class ErrorResponse:
    """Standardized error response format"""
    
    @staticmethod
    def create_error_response(
        status_code: int,
        message: str,
        detail: str = None,
        errors: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        response = {
            "success": False,
            "message": message,
            "status_code": status_code
        }
        
        if detail:
            response["detail"] = detail
            
        if errors:
            response["errors"] = errors
            
        return response

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with consistent format"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail} - {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse.create_error_response(
            status_code=exc.status_code,
            message="Request failed",
            detail=exc.detail
        )
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation errors with detailed field information"""
    logger.warning(f"Validation Error: {exc.errors()} - {request.url}")
    
    # Format validation errors for better client understanding
    formatted_errors = {}
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])  # Skip 'body' prefix
        formatted_errors[field] = error["msg"]
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse.create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation failed",
            detail="Please check your input data",
            errors=formatted_errors
        )
    )

async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle database errors"""
    logger.error(f"Database Error: {str(exc)} - {request.url}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse.create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Database operation failed",
            detail="Please try again later"
        )
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other unexpected exceptions"""
    logger.error(f"Unexpected Error: {str(exc)} - {request.url}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse.create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            detail="An unexpected error occurred"
        )
    )