"""Dependency injection container and wiring"""
from functools import lru_cache
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.adapters.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.adapters.sqlalchemy_post_repository import SqlAlchemyPostReadRepository, SqlAlchemyPostWriteRepository
from app.adapters.services import BcryptPasswordHasher, JWTTokenService, DefaultSlugGenerator, MockEmailSender
from app.use_cases.auth import RegisterUserUseCase, LoginUserUseCase, GetUserByTokenUseCase
from app.use_cases.posts import (
    CreatePostUseCase, UpdatePostUseCase, GetPostUseCase, 
    GetPostBySlugUseCase, ListPostsUseCase, DeletePostUseCase, PublishPostUseCase
)


class Container:
    """Dependency injection container"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Initialize services (singletons)
        self._password_hasher = BcryptPasswordHasher()
        self._token_service = JWTTokenService()
        self._slug_generator = DefaultSlugGenerator()
        self._email_sender = MockEmailSender()
        
        # Initialize repositories
        self._user_repository = SqlAlchemyUserRepository(db)
        self._post_read_repository = SqlAlchemyPostReadRepository(db)
        self._post_write_repository = SqlAlchemyPostWriteRepository(db)
    
    # Service accessors
    @property
    def password_hasher(self):
        return self._password_hasher
    
    @property
    def token_service(self):
        return self._token_service
    
    @property
    def slug_generator(self):
        return self._slug_generator
    
    @property
    def email_sender(self):
        return self._email_sender
    
    # Repository accessors
    @property
    def user_repository(self):
        return self._user_repository
    
    @property
    def post_read_repository(self):
        return self._post_read_repository
    
    @property
    def post_write_repository(self):
        return self._post_write_repository
    
    # Use case factories (create new instances each time)
    def register_user_use_case(self) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            self.user_repository,
            self.password_hasher,
            self.token_service
        )
    
    def login_user_use_case(self) -> LoginUserUseCase:
        return LoginUserUseCase(
            self.user_repository,
            self.password_hasher,
            self.token_service
        )
    
    def get_user_by_token_use_case(self) -> GetUserByTokenUseCase:
        return GetUserByTokenUseCase(
            self.user_repository,
            self.token_service
        )
    
    def create_post_use_case(self) -> CreatePostUseCase:
        return CreatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
    
    def update_post_use_case(self) -> UpdatePostUseCase:
        return UpdatePostUseCase(
            self.post_read_repository,
            self.post_write_repository,
            self.slug_generator
        )
    
    def get_post_use_case(self) -> GetPostUseCase:
        return GetPostUseCase(
            self.post_read_repository,
            self.post_write_repository
        )
    
    def get_post_by_slug_use_case(self) -> GetPostBySlugUseCase:
        return GetPostBySlugUseCase(
            self.post_read_repository,
            self.post_write_repository
        )
    
    def list_posts_use_case(self) -> ListPostsUseCase:
        return ListPostsUseCase(self.post_read_repository)
    
    def delete_post_use_case(self) -> DeletePostUseCase:
        return DeletePostUseCase(
            self.post_read_repository,
            self.post_write_repository
        )
    
    def publish_post_use_case(self) -> PublishPostUseCase:
        return PublishPostUseCase(
            self.post_read_repository,
            self.post_write_repository
        )


def get_container(db: Session = None) -> Container:
    """Get DI container instance"""
    if db is None:
        db = next(get_db())
    return Container(db)