"""
Gamification Router
Handles achievement badges and leaderboard
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from models.achievement import Achievement
from models.reading_activity import PreReading, Practice
from auth.dependencies import get_current_user

router = APIRouter(prefix="/gamification", tags=["gamification"])

# Badge definitions
BADGE_CRITERIA = {
    "first_step": {
        "name": "İlk Adım",
        "description": "İlk hikayeni okudun!",
        "icon": "🌟",
        "color": "gold",
        "check": lambda user_id, db: get_story_count(user_id, db) >= 1
    },
    "speed_reader": {
        "name": "Hızlı Okuyucu",
        "description": "5 hikaye okudun",
        "icon": "⚡",
        "color": "blue",
        "check": lambda user_id, db: get_story_count(user_id, db) >= 5
    },
    "bookworm": {
        "name": "Kitap Kurdu",
        "description": "10 hikaye okudun",
        "icon": "📚",
        "color": "purple",
        "check": lambda user_id, db: get_story_count(user_id, db) >= 10
    },
    "super_reader": {
        "name": "Süper Okuyucu",
        "description": "25 hikaye okudun",
        "icon": "🦸",
        "color": "red",
        "check": lambda user_id, db: get_story_count(user_id, db) >= 25
    },
    "master": {
        "name": "Ustalaşma",
        "description": "50 hikaye okudun",
        "icon": "👑",
        "color": "gold",
        "check": lambda user_id, db: get_story_count(user_id, db) >= 50
    },
    "practice_master": {
        "name": "Pratik Ustası",
        "description": "10 pratik tamamladın",
        "icon": "🎯",
        "color": "green",
        "check": lambda user_id, db: get_practice_count(user_id, db) >= 10
    },
    "speed_champion": {
        "name": "Hız Şampiyonu",
        "description": "150+ kelime/dakika hıza ulaştın",
        "icon": "🏃",
        "color": "orange",
        "check": lambda user_id, db: get_avg_speed(user_id, db) >= 150
    },
    "perfect_comprehension": {
        "name": "Mükemmel Anlama",
        "description": "Anlama puanında 9+ aldın",
        "icon": "🧠",
        "color": "pink",
        "check": lambda user_id, db: get_avg_comprehension(user_id, db) >= 9
    }
}

def get_story_count(user_id: int, db: Session) -> int:
    """Get unique story count for user"""
    count = db.query(func.count(func.distinct(PreReading.story_id))).filter(
        PreReading.ogrenci_id == user_id
    ).scalar()
    return count or 0

def get_practice_count(user_id: int, db: Session) -> int:
    """Get total practice sessions for user"""
    count = db.query(func.count(Practice.id)).filter(
        Practice.ogrenci_id == user_id
    ).scalar()
    return count or 0

def get_avg_speed(user_id: int, db: Session) -> float:
    """Get average reading speed for user"""
    avg = db.query(func.avg(PreReading.okuma_hizi)).filter(
        PreReading.ogrenci_id == user_id,
        PreReading.okuma_hizi.isnot(None)
    ).scalar()
    return float(avg) if avg else 0.0

def get_avg_comprehension(user_id: int, db: Session) -> float:
    """Get average comprehension score for user"""
    # TODO: Implement when evaluation system is ready
    return 0.0

def has_badge(user_id: int, badge_type: str, db: Session) -> bool:
    """Check if user already has badge"""
    exists = db.query(Achievement).filter(
        Achievement.user_id == user_id,
        Achievement.badge_type == badge_type
    ).first()
    return exists is not None

def award_badge(user_id: int, badge_type: str, db: Session):
    """Award badge to user"""
    if not has_badge(user_id, badge_type, db):
        achievement = Achievement(
            user_id=user_id,
            badge_type=badge_type
        )
        db.add(achievement)
        db.commit()
        return True
    return False

@router.get("/badges/me")
async def get_my_badges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all badges earned by current user"""
    achievements = db.query(Achievement).filter(
        Achievement.user_id == current_user.id
    ).order_by(Achievement.earned_at.desc()).all()
    
    badges = []
    for achievement in achievements:
        badge_info = BADGE_CRITERIA.get(achievement.badge_type, {})
        badges.append({
            "type": achievement.badge_type,
            "name": badge_info.get("name", achievement.badge_type),
            "description": badge_info.get("description", ""),
            "icon": badge_info.get("icon", "🏅"),
            "color": badge_info.get("color", "gray"),
            "earned_at": achievement.earned_at.isoformat()
        })
    
    return {"badges": badges, "total": len(badges)}

@router.post("/check-achievements")
async def check_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user earned new achievements"""
    new_badges = []
    
    for badge_type, criteria in BADGE_CRITERIA.items():
        # Skip if already has badge
        if has_badge(current_user.id, badge_type, db):
            continue
        
        # Check if criteria met
        if criteria["check"](current_user.id, db):
            if award_badge(current_user.id, badge_type, db):
                new_badges.append({
                    "type": badge_type,
                    "name": criteria["name"],
                    "description": criteria["description"],
                    "icon": criteria["icon"],
                    "color": criteria["color"]
                })
    
    return {"new_badges": new_badges}

@router.get("/leaderboard")
async def get_leaderboard(
    period: str = "weekly",
    grade_level: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get leaderboard rankings"""
    # Calculate date range
    now = datetime.utcnow()
    if period == "weekly":
        start_date = now - timedelta(days=7)
    elif period == "monthly":
        start_date = now - timedelta(days=30)
    else:  # all_time
        start_date = datetime(2000, 1, 1)
    
    # Base query
    query = db.query(
        User.id,
        User.ad_soyad,
        User.sinif_duzeyi,
        func.count(func.distinct(PreReading.story_id)).label('story_count'),
        func.avg(PreReading.okuma_hizi).label('avg_speed'),
        func.coalesce(func.avg(0), 0).label('avg_comprehension')  # Placeholder
    ).join(
        PreReading, User.id == PreReading.ogrenci_id
    ).filter(
        User.rol == 'ogrenci',
        PreReading.created_at >= start_date
    )
    
    # Filter by grade if specified
    if grade_level:
        query = query.filter(User.sinif_duzeyi == grade_level)
    
    # Group and order
    leaderboard = query.group_by(
        User.id, User.ad_soyad, User.sinif_duzeyi
    ).order_by(
        desc('story_count'),
        desc('avg_speed')
    ).limit(limit).all()
    
    # Format results
    results = []
    for rank, entry in enumerate(leaderboard, 1):
        results.append({
            "rank": rank,
            "user_id": entry.id,
            "name": entry.ad_soyad,
            "grade_level": entry.sinif_duzeyi,
            "story_count": entry.story_count,
            "avg_speed": round(entry.avg_speed, 1) if entry.avg_speed else 0,
            "avg_comprehension": round(entry.avg_comprehension, 1) if entry.avg_comprehension else 0
        })
    
    return {"leaderboard": results, "period": period}

@router.get("/progress/me")
async def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress towards next milestone"""
    story_count = get_story_count(current_user.id, db)
    
    # Define milestones
    milestones = [1, 5, 10, 25, 50, 100]
    
    # Find next milestone
    next_milestone = None
    for milestone in milestones:
        if story_count < milestone:
            next_milestone = milestone
            break
    
    if next_milestone is None:
        next_milestone = milestones[-1]
    
    progress_percentage = (story_count / next_milestone) * 100 if next_milestone > 0 else 100
    
    return {
        "current_stories": story_count,
        "next_milestone": next_milestone,
        "remaining": max(0, next_milestone - story_count),
        "progress_percentage": min(100, progress_percentage)
    }
