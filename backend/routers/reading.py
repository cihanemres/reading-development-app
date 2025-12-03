from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models.user import User, UserRole
from models.reading_activity import PreReading, Practice, Answer
from models.story import Story
from auth.dependencies import get_current_user
from utils.word_counter import calculate_reading_speed
from utils.progress_calculator import calculate_improvement

router = APIRouter(prefix="/api/reading", tags=["Reading Activities"])

# Pydantic schemas
class PreReadingCreate(BaseModel):
    story_id: int
    okuma_suresi: float  # in seconds
    kelime_sayisi: int

class PracticeCreate(BaseModel):
    story_id: int
    okuma_suresi: float
    kelime_sayisi: int

class AnswerCreate(BaseModel):
    story_id: int
    q1: Optional[str] = None
    q2: Optional[str] = None
    q3: Optional[str] = None
    q4: Optional[str] = None
    acik_uclu: Optional[str] = None

class ReadingResponse(BaseModel):
    id: int
    ogrenci_id: int
    story_id: int
    okuma_suresi: float
    kelime_sayisi: int
    okuma_hizi: Optional[float]
    
    class Config:
        from_attributes = True

class PracticeResponse(ReadingResponse):
    tekrar_no: int

class AnswerResponse(BaseModel):
    id: int
    ogrenci_id: int
    story_id: int
    q1: Optional[str]
    q2: Optional[str]
    q3: Optional[str]
    q4: Optional[str]
    acik_uclu: Optional[str]
    
    class Config:
        from_attributes = True

@router.post("/pre-reading", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
async def save_pre_reading(
    data: PreReadingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Save pre-reading (initial reading) data
    """
    # Verify story exists
    story = db.query(Story).filter(Story.id == data.story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    
    # Check if student already has pre-reading for this story
    existing = db.query(PreReading).filter(
        PreReading.ogrenci_id == current_user.id,
        PreReading.story_id == data.story_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pre-reading already exists for this story. Use practice endpoint instead."
        )
    
    # Calculate reading speed
    reading_speed = calculate_reading_speed(data.kelime_sayisi, data.okuma_suresi)
    
    # Create pre-reading record
    pre_reading = PreReading(
        ogrenci_id=current_user.id,
        story_id=data.story_id,
        okuma_suresi=data.okuma_suresi,
        kelime_sayisi=data.kelime_sayisi,
        okuma_hizi=reading_speed
    )
    
    db.add(pre_reading)
    db.commit()
    db.refresh(pre_reading)
    
    return pre_reading

@router.post("/practice", response_model=PracticeResponse, status_code=status.HTTP_201_CREATED)
async def save_practice(
    data: PracticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Save practice reading data
    """
    # Verify story exists
    story = db.query(Story).filter(Story.id == data.story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    
    # Get the next practice number
    last_practice = db.query(Practice).filter(
        Practice.ogrenci_id == current_user.id,
        Practice.story_id == data.story_id
    ).order_by(Practice.tekrar_no.desc()).first()
    
    next_number = 1 if not last_practice else last_practice.tekrar_no + 1
    
    # Calculate reading speed
    reading_speed = calculate_reading_speed(data.kelime_sayisi, data.okuma_suresi)
    
    # Create practice record
    practice = Practice(
        ogrenci_id=current_user.id,
        story_id=data.story_id,
        tekrar_no=next_number,
        okuma_suresi=data.okuma_suresi,
        kelime_sayisi=data.kelime_sayisi,
        okuma_hizi=reading_speed
    )
    
    db.add(practice)
    db.commit()
    db.refresh(practice)
    
    return practice

@router.post("/answers", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
async def save_answers(
    data: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Save quiz answers
    """
    # Verify story exists
    story = db.query(Story).filter(Story.id == data.story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    
    # Calculate score
    from models.quiz import QuizQuestion
    questions = db.query(QuizQuestion).filter(QuizQuestion.story_id == data.story_id).order_by(QuizQuestion.id).all()
    correct_count = 0
    
    # Map answers to indices (assuming questions are ordered by ID)
    student_answers = [data.q1, data.q2, data.q3, data.q4]
    
    for i, q in enumerate(questions):
        if i < 4:  # Only check first 4 questions (multiple choice)
            student_ans = student_answers[i]
            if student_ans and student_ans == q.correct_answer:
                correct_count += 1

    # Check if answers already exist
    existing = db.query(Answer).filter(
        Answer.ogrenci_id == current_user.id,
        Answer.story_id == data.story_id
    ).first()
    
    if existing:
        # Update existing answers
        existing.q1 = data.q1
        existing.q2 = data.q2
        existing.q3 = data.q3
        existing.q4 = data.q4
        existing.acik_uclu = data.acik_uclu
        existing.dogru_sayisi = correct_count
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new answer record
    answer = Answer(
        ogrenci_id=current_user.id,
        story_id=data.story_id,
        q1=data.q1,
        q2=data.q2,
        q3=data.q3,
        q4=data.q4,
        acik_uclu=data.acik_uclu,
        dogru_sayisi=correct_count
    )
    
    db.add(answer)
    db.commit()
    db.refresh(answer)
    
    return answer

@router.get("/progress/{story_id}")
async def get_reading_progress(
    story_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get reading progress for a specific story
    """
    improvement = calculate_improvement(current_user.id, story_id, db)
    
    # Get all practice attempts
    practices = db.query(Practice).filter(
        Practice.ogrenci_id == current_user.id,
        Practice.story_id == story_id
    ).order_by(Practice.tekrar_no).all()
    
    practice_data = [
        {
            "attempt": p.tekrar_no,
            "speed_wpm": p.okuma_hizi,
            "time_seconds": p.okuma_suresi
        }
        for p in practices
    ]
    
    return {
        "story_id": story_id,
        "improvement": improvement,
        "practice_history": practice_data
    }

@router.get("/my-progress")
async def get_overall_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get overall reading progress for the current student
    """
    from utils.progress_calculator import get_student_progress_summary
    
    summary = get_student_progress_summary(current_user.id, db)
    
    # Get all stories the student has read
    pre_readings = db.query(PreReading).filter(
        PreReading.ogrenci_id == current_user.id
    ).all()
    
    stories_read = []
    for pr in pre_readings:
        story = db.query(Story).filter(Story.id == pr.story_id).first()
        if story:
            improvement = calculate_improvement(current_user.id, story.id, db)
            stories_read.append({
                "story_id": story.id,
                "story_title": story.baslik,
                "improvement": improvement
            })
    
    return {
        "summary": summary,
        "stories": stories_read
    }
