from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL") or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/okuma_db")

# Debug: Print the database URL (will show in logs)
print(f"DATABASE_URL configured: {DATABASE_URL[:50]}..." if DATABASE_URL else "DATABASE_URL not set!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    """
    Database session dependency for FastAPI routes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables
    """
    # Import all models to ensure they are registered with Base
    from models.user import User
    from models.story import Story
    from models.reading_activity import PreReading, Answer
    from models.evaluation import TeacherEvaluation
    from models.quiz import QuizQuestion
    
    Base.metadata.create_all(bind=engine)
