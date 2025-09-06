# SOLID Architecture Implementation

## Overview

This implementation follows SOLID principles with a Clean Architecture approach, separating business logic from infrastructure concerns.

## Architecture Layers

### 1. Domain Layer (`app/domain/`)
- **Purpose**: Pure business logic and entities
- **Components**:
  - `entities.py`: Domain entities (User, BlogPost, Tag, Category)
  - `errors.py`: Domain-specific exceptions
- **Dependencies**: None (pure Python)

### 2. Use Cases Layer (`app/use_cases/`)
- **Purpose**: Application business logic and orchestration
- **Components**:
  - `auth.py`: User registration, login, token validation
  - `posts.py`: Post CRUD operations and publishing
- **Dependencies**: Domain layer, Ports (abstractions only)

### 3. Ports Layer (`app/ports/`)
- **Purpose**: Interface definitions for dependency inversion
- **Components**:
  - `repositories.py`: Repository interfaces using Python Protocols
  - `services.py`: Service interfaces (password hashing, tokens, etc.)
- **Dependencies**: Domain layer

### 4. Adapters Layer (`app/adapters/`)
- **Purpose**: Infrastructure implementations
- **Components**:
  - `sqlalchemy_user_repository.py`: SQLAlchemy user persistence
  - `sqlalchemy_post_repository.py`: SQLAlchemy post persistence  
  - `services.py`: Bcrypt, JWT, slug generation implementations
  - `memory_repositories.py`: In-memory implementations for testing
- **Dependencies**: Ports, Domain, External libraries

### 5. Presentation Layer (`app/presentation/`)
- **Purpose**: HTTP request/response handling
- **Components**:
  - `routers/auth.py`: Authentication endpoints
  - `routers/posts.py`: Post management endpoints
  - `schemas.py`: Pydantic request/response models
- **Dependencies**: Use cases, Domain

### 6. Configuration Layer (`app/config/`)
- **Purpose**: Dependency injection and wiring
- **Components**:
  - `container.py`: DI container for managing dependencies
- **Dependencies**: All layers

## Request Flow

```
HTTP Request → Router → Use Case → Repository/Service → Database/External Service
                ↓
HTTP Response ← DTO ← Domain Entity ← Domain Entity ← Data
```

### Example: Create Post Flow

1. **Router** (`presentation/routers/posts.py`):
   - Receives HTTP POST request
   - Validates request using Pydantic schema
   - Maps request to use case input

2. **Use Case** (`use_cases/posts.py`):
   - Validates business rules
   - Generates slug using service
   - Creates domain entity
   - Calls repository to persist

3. **Repository** (`adapters/sqlalchemy_post_repository.py`):
   - Converts domain entity to SQLAlchemy model
   - Saves to database
   - Returns domain entity

4. **Router**:
   - Maps domain entity to response DTO
   - Returns HTTP response

## SOLID Principles Implementation

### Single Responsibility (S)
- Each use case handles one business operation
- Routers only handle HTTP concerns
- Repositories only handle data persistence

### Open/Closed (O)
- New repository implementations can be added without changing use cases
- New authentication methods can be added via service interfaces

### Liskov Substitution (L)
- All repository implementations satisfy the same Protocol interface
- In-memory and SQLAlchemy repositories are interchangeable

### Interface Segregation (I)
- Separate read/write repository interfaces
- Service interfaces are focused and minimal

### Dependency Inversion (D)
- Use cases depend on port abstractions, not concrete implementations
- DI container wires concrete implementations at runtime

## Testing Strategy

### Unit Tests
- Use cases tested with in-memory adapters
- No database or external service dependencies
- Fast and reliable test execution

### Integration Tests
- Test adapters with real database
- Verify repository implementations work correctly

### Contract Tests
- Ensure all adapters satisfy port interfaces
- Verify Liskov substitution principle

## Benefits

1. **Testability**: Business logic is easily testable without infrastructure
2. **Flexibility**: Can swap implementations (SQLite ↔ PostgreSQL ↔ In-memory)
3. **Maintainability**: Clear separation of concerns
4. **Extensibility**: Easy to add new features following established patterns
5. **Independence**: Domain logic doesn't depend on frameworks or databases

## Migration from Legacy Code

The new architecture coexists with the legacy code. To complete the migration:

1. Update `main.py` to use new routers
2. Replace old routers with new implementation
3. Migrate remaining features (comments, categories, etc.)
4. Remove legacy code once all features are migrated

## Usage Examples

### Creating a Post
```python
# In the router
container = get_container(db)
use_case = container.create_post_use_case()

request = CreatePostRequest(
    title="My Post",
    content="Post content",
    author_id=current_user.id
)

post = use_case.execute(request)
```

### Testing a Use Case
```python
# Unit test with in-memory repository
user_repo = InMemoryUserRepository()
password_hasher = BcryptPasswordHasher()
token_service = JWTTokenService()

use_case = RegisterUserUseCase(user_repo, password_hasher, token_service)
response = use_case.execute(request)

assert response.user.username == "testuser"
```