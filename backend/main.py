from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

from database import init_db
from routers import auth, stories, reading, teacher, parent, admin, notifications, export, gamification, assignments
import migration_script

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Okuma Geliştirme Uygulaması",
    description="Reading Development Web Application API",
    version="1.0.0"
)

# CORS Configuration
# Use env var for specific origins (wildcard doesn't work with credentials)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://okuma-frontend.onrender.com").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
os.makedirs("static/uploads/images", exist_ok=True)
os.makedirs("static/uploads/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(stories.router)
app.include_router(reading.router)
app.include_router(teacher.router)
app.include_router(parent.router)
app.include_router(admin.router)
app.include_router(notifications.router)
app.include_router(export.router)
app.include_router(gamification.router)
app.include_router(assignments.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    try:
        migration_script.run_migration()
        print("✅ Migration executed successfully")
    except Exception as e:
        print(f"⚠️ Migration failed: {e}")
        
    print("✅ Database initialized successfully")
    print("🚀 Application started")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Okuma Geliştirme Uygulaması API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
