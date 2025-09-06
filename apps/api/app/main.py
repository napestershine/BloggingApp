from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from app.database.connection import engine, Base
from app.models import models
from app.routers import auth, users, blog_posts, comments, post_likes, post_sharing, media, categories, tags, notifications
from app.core.config import settings

# SQLAdmin setup
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from app.models.models import User, BlogPost, Comment

# Create database tables (for development - use Alembic migrations in production)
# Note: This is commented out for async usage - use Alembic migrations instead
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A FastAPI-based blog API with JWT authentication",
    version="1.0.0",
    openapi_url="/openapi.json",  # Explicitly set OpenAPI URL
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blog_posts.router)
app.include_router(comments.router)
app.include_router(post_likes.router)
app.include_router(post_sharing.router)
app.include_router(media.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(notifications.router)

# SQLAdmin Authentication Backend
class AdminAuth(AuthenticationBackend):
    async def login(self, request):
        # Simple admin authentication - in production, use proper auth
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        
        # For demo purposes - replace with proper authentication
        if username == "admin" and password == "admin":
            request.session.update({"token": "admin-authenticated"})
            return True
        return False

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        token = request.session.get("token")
        return token == "admin-authenticated"

# Set up SQLAdmin
authentication_backend = AdminAuth(secret_key=settings.secret_key.get_secret_value())
admin = Admin(app, engine, authentication_backend=authentication_backend, title="Blog Admin")

# Add model views to admin
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active, User.created_at]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.created_at]

class BlogPostAdmin(ModelView, model=BlogPost):
    column_list = [BlogPost.id, BlogPost.title, BlogPost.author, BlogPost.created_at, BlogPost.is_draft]
    column_searchable_list = [BlogPost.title, BlogPost.content]
    column_sortable_list = [BlogPost.id, BlogPost.title, BlogPost.created_at]

class CommentAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.content, Comment.author, Comment.blog_post, Comment.created_at]
    column_searchable_list = [Comment.content]
    column_sortable_list = [Comment.id, Comment.created_at]

admin.add_view(UserAdmin)
admin.add_view(BlogPostAdmin)
admin.add_view(CommentAdmin)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Ensure OpenAPI JSON is available
@app.get("/openapi.json", include_in_schema=False)
def get_openapi():
    return app.openapi()