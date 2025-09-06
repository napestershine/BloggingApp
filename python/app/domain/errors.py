"""Domain-specific errors"""


class DomainError(Exception):
    """Base domain error"""
    pass


class ValidationError(DomainError):
    """Domain validation error"""
    pass


class NotFoundError(DomainError):
    """Resource not found error"""
    pass


class ConflictError(DomainError):
    """Resource conflict error"""
    pass


class UnauthorizedError(DomainError):
    """Access denied error"""
    pass


# User-specific errors
class UserNotFoundError(NotFoundError):
    """User not found"""
    def __init__(self, identifier: str):
        super().__init__(f"User not found: {identifier}")


class UserAlreadyExistsError(ConflictError):
    """User already exists"""
    def __init__(self, field: str, value: str):
        super().__init__(f"User with {field} '{value}' already exists")


class InvalidCredentialsError(UnauthorizedError):
    """Invalid login credentials"""
    def __init__(self):
        super().__init__("Invalid username or password")


class WeakPasswordError(ValidationError):
    """Password doesn't meet security requirements"""
    def __init__(self, requirements: str):
        super().__init__(f"Password doesn't meet requirements: {requirements}")


# Post-specific errors
class PostNotFoundError(NotFoundError):
    """Post not found"""
    def __init__(self, identifier: str):
        super().__init__(f"Post not found: {identifier}")


class PostAlreadyExistsError(ConflictError):
    """Post with same title/slug already exists"""
    def __init__(self, field: str, value: str):
        super().__init__(f"Post with {field} '{value}' already exists")


class InvalidPostStatusError(ValidationError):
    """Invalid post status transition"""
    def __init__(self, current_status: str, target_status: str):
        super().__init__(f"Cannot change post status from {current_status} to {target_status}")


class PostNotPublishableError(ValidationError):
    """Post cannot be published in current state"""
    def __init__(self, reason: str):
        super().__init__(f"Post cannot be published: {reason}")


class UnauthorizedPostAccessError(UnauthorizedError):
    """User not authorized to access post"""
    def __init__(self, action: str):
        super().__init__(f"Not authorized to {action} this post")