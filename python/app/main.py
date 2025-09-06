import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_engine
from app.models import models
from app.routers import auth, users, blog_posts, comments, search, seo, sitemap, slugs, recommendations, feed, rss, post_likes, post_sharing, media, categories, tags, user_follows, notification_system, bookmarks

# Import middleware and error handlers
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)
from app.schemas.responses import HealthCheckResponse
from app.services.health_service import health_service
from app.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create database tables (only if database is available)
try:
    engine = get_engine()
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    logging.warning(f"Database not available during startup: {str(e)}")

app = FastAPI(
    title="Blog API",
    description="A FastAPI-based blog API with JWT authentication, SEO, and discovery features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware
app.add_middleware(LoggingMiddleware)

# Add CORS middleware with configurable origins
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Use parsed origins property
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

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

# Include existing enhanced routers
app.include_router(search.router)
app.include_router(seo.router)
app.include_router(sitemap.router)
app.include_router(slugs.router)
app.include_router(recommendations.router)
app.include_router(feed.router)
app.include_router(rss.router)

# Include new social features routers
app.include_router(user_follows.router)

# Import and include notifications router
from app.routers import notifications
app.include_router(notifications.router)
app.include_router(notification_system.router)
app.include_router(bookmarks.router)

# Import and include admin routers
from app.admin import users as admin_users, content as admin_content
app.include_router(admin_users.router)
app.include_router(admin_content.router)

# Include new SEO & Discovery routers
app.include_router(search.router, prefix="/api")
app.include_router(seo.router, prefix="/api")
app.include_router(sitemap.router, prefix="/api")
app.include_router(slugs.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(feed.router, prefix="/api")
app.include_router(rss.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API", "status": "healthy", "version": "1.0.0"}

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint that returns system status and basic metrics
    """
    return await health_service.get_health_status()
