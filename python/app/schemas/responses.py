"""
Standard response models for consistent API responses
"""
from typing import Generic, TypeVar, Any, Optional, Dict
from pydantic import BaseModel, Field

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    """Base response model for all API responses"""
    success: bool = Field(default=True, description="Indicates if the request was successful")
    message: str = Field(description="Human-readable message")
    data: Optional[T] = Field(default=None, description="Response data")

class SuccessResponse(BaseResponse[T]):
    """Standard success response"""
    success: bool = Field(default=True)

class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = Field(default=False)
    message: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    errors: Optional[Dict[str, Any]] = Field(default=None, description="Field-specific errors")
    status_code: int = Field(description="HTTP status code")

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    items: list[T] = Field(description="List of items")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    size: int = Field(description="Number of items per page")
    pages: int = Field(description="Total number of pages")

class CreatedResponse(BaseResponse[T]):
    """Response for successful creation"""
    success: bool = Field(default=True)
    message: str = Field(default="Resource created successfully")

class UpdatedResponse(BaseResponse[T]):
    """Response for successful update"""
    success: bool = Field(default=True)
    message: str = Field(default="Resource updated successfully")

class DeletedResponse(BaseModel):
    """Response for successful deletion"""
    success: bool = Field(default=True)
    message: str = Field(default="Resource deleted successfully")

class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str = Field(description="Service status")
    timestamp: str = Field(description="Current timestamp")
    version: str = Field(description="API version")
    uptime: float = Field(description="Service uptime in seconds")
    database: str = Field(description="Database connection status")
    dependencies: Dict[str, str] = Field(description="Status of external dependencies")