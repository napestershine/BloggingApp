from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine
from app.models import models
from app.routers import auth, users, blog_posts, comments

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

# Import and include notifications router
from app.routers import notifications
app.include_router(notifications.router)

# Import and include admin routers
from app.admin import users as admin_users, content as admin_content
app.include_router(admin_users.router)
app.include_router(admin_content.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}