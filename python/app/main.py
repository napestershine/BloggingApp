from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine
from app.models import models
from app.routers import auth, users, blog_posts, comments, post_likes, post_sharing, media, categories, tags, search, user_follows, notification_system, bookmarks

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A FastAPI-based blog API with JWT authentication",
    version="1.0.0"
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
app.include_router(search.router)
app.include_router(user_follows.router)

# Import and include notifications router
from app.routers import notifications
app.include_router(notifications.router)
app.include_router(notification_system.router)
app.include_router(bookmarks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}