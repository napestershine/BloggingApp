"""Unit tests for auth use cases using in-memory repositories"""
import pytest
from app.use_cases.auth import RegisterUserUseCase, LoginUserUseCase, GetUserByTokenUseCase
from app.use_cases.auth import RegisterUserRequest, LoginRequest
from app.adapters.memory_repositories import InMemoryUserRepository
from app.adapters.services import BcryptPasswordHasher, JWTTokenService
from app.domain.errors import UserAlreadyExistsError, InvalidCredentialsError, WeakPasswordError


class TestRegisterUserUseCase:
    """Test user registration use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.user_repository = InMemoryUserRepository()
        self.password_hasher = BcryptPasswordHasher()
        self.token_service = JWTTokenService()
        self.use_case = RegisterUserUseCase(
            self.user_repository,
            self.password_hasher,
            self.token_service
        )
    
    def test_register_user_success(self):
        """Test successful user registration"""
        request = RegisterUserRequest(
            username="testuser",
            email="test@example.com",
            name="Test User",
            password="password123",
            retyped_password="password123"
        )
        
        response = self.use_case.execute(request)
        
        assert response.user.username == "testuser"
        assert response.user.email == "test@example.com"
        assert response.user.name == "Test User"
        assert response.user.id is not None
        assert response.access_token is not None
        assert response.token_type == "bearer"
    
    def test_register_user_password_mismatch(self):
        """Test registration with mismatched passwords"""
        request = RegisterUserRequest(
            username="testuser",
            email="test@example.com",
            name="Test User",
            password="password123",
            retyped_password="different"
        )
        
        with pytest.raises(WeakPasswordError):
            self.use_case.execute(request)
    
    def test_register_user_weak_password(self):
        """Test registration with weak password"""
        request = RegisterUserRequest(
            username="testuser",
            email="test@example.com",
            name="Test User",
            password="123",
            retyped_password="123"
        )
        
        with pytest.raises(WeakPasswordError):
            self.use_case.execute(request)
    
    def test_register_duplicate_username(self):
        """Test registration with duplicate username"""
        # Register first user
        request1 = RegisterUserRequest(
            username="testuser",
            email="test1@example.com",
            name="Test User 1",
            password="password123",
            retyped_password="password123"
        )
        self.use_case.execute(request1)
        
        # Try to register with same username
        request2 = RegisterUserRequest(
            username="testuser",
            email="test2@example.com",
            name="Test User 2",
            password="password123",
            retyped_password="password123"
        )
        
        with pytest.raises(UserAlreadyExistsError):
            self.use_case.execute(request2)
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        # Register first user
        request1 = RegisterUserRequest(
            username="testuser1",
            email="test@example.com",
            name="Test User 1",
            password="password123",
            retyped_password="password123"
        )
        self.use_case.execute(request1)
        
        # Try to register with same email
        request2 = RegisterUserRequest(
            username="testuser2",
            email="test@example.com",
            name="Test User 2",
            password="password123",
            retyped_password="password123"
        )
        
        with pytest.raises(UserAlreadyExistsError):
            self.use_case.execute(request2)


class TestLoginUserUseCase:
    """Test user login use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.user_repository = InMemoryUserRepository()
        self.password_hasher = BcryptPasswordHasher()
        self.token_service = JWTTokenService()
        
        # Create test user
        self.register_use_case = RegisterUserUseCase(
            self.user_repository,
            self.password_hasher,
            self.token_service
        )
        
        register_request = RegisterUserRequest(
            username="testuser",
            email="test@example.com",
            name="Test User",
            password="password123",
            retyped_password="password123"
        )
        self.test_user_response = self.register_use_case.execute(register_request)
        
        self.login_use_case = LoginUserUseCase(
            self.user_repository,
            self.password_hasher,
            self.token_service
        )
    
    def test_login_with_username_success(self):
        """Test successful login with username"""
        request = LoginRequest(
            username="testuser",
            password="password123"
        )
        
        response = self.login_use_case.execute(request)
        
        assert response.user.username == "testuser"
        assert response.access_token is not None
        assert response.token_type == "bearer"
    
    def test_login_with_email_success(self):
        """Test successful login with email"""
        request = LoginRequest(
            username="test@example.com",
            password="password123"
        )
        
        response = self.login_use_case.execute(request)
        
        assert response.user.email == "test@example.com"
        assert response.access_token is not None
    
    def test_login_invalid_username(self):
        """Test login with non-existent username"""
        request = LoginRequest(
            username="nonexistent",
            password="password123"
        )
        
        with pytest.raises(InvalidCredentialsError):
            self.login_use_case.execute(request)
    
    def test_login_invalid_password(self):
        """Test login with wrong password"""
        request = LoginRequest(
            username="testuser",
            password="wrongpassword"
        )
        
        with pytest.raises(InvalidCredentialsError):
            self.login_use_case.execute(request)


class TestGetUserByTokenUseCase:
    """Test get user by token use case"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.user_repository = InMemoryUserRepository()
        self.password_hasher = BcryptPasswordHasher()
        self.token_service = JWTTokenService()
        
        # Create test user
        register_use_case = RegisterUserUseCase(
            self.user_repository,
            self.password_hasher,
            self.token_service
        )
        
        register_request = RegisterUserRequest(
            username="testuser",
            email="test@example.com",
            name="Test User",
            password="password123",
            retyped_password="password123"
        )
        self.test_user_response = register_use_case.execute(register_request)
        
        self.use_case = GetUserByTokenUseCase(
            self.user_repository,
            self.token_service
        )
    
    def test_get_user_by_valid_token(self):
        """Test getting user with valid token"""
        token = self.test_user_response.access_token
        
        user = self.use_case.execute(token)
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_get_user_by_invalid_token(self):
        """Test getting user with invalid token"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(InvalidCredentialsError):
            self.use_case.execute(invalid_token)