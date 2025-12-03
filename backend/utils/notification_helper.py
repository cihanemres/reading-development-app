"""
Notification Helper Functions
Utility functions for creating and managing notifications
"""
from sqlalchemy.orm import Session
from models.notification import Notification
from models.user import User

def create_notification(
    db: Session,
    user_id: int,
    type: str,
    title: str,
    message: str,
    link: str = None
) -> Notification:
    """
    Create a new notification
    
    Args:
        db: Database session
        user_id: ID of user to notify
        type: Notification type (evaluation, progress, achievement, general)
        title: Notification title
        message: Notification message
        link: Optional link to related content
        
    Returns:
        Created notification object
    """
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        link=link
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return notification

def notify_parent_of_evaluation(
    db: Session,
    student_id: int,
    teacher_name: str,
    story_title: str = None
):
    """
    Notify parent when teacher evaluates their child
    
    Args:
        db: Database session
        student_id: ID of the student
        teacher_name: Name of the teacher who evaluated
        story_title: Optional story title
    """
    # Get student
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        return
    
    # Get parent
    parent = db.query(User).filter(User.id == student.veli_id).first()
    if not parent:
        return
    
    # Create notification
    title = "Yeni Öğretmen Değerlendirmesi"
    message = f"{teacher_name}, {student.ad_soyad} için yeni bir değerlendirme yaptı"
    if story_title:
        message += f" ({story_title})"
    
    create_notification(
        db=db,
        user_id=parent.id,
        type="evaluation",
        title=title,
        message=message,
        link="/parent/dashboard"
    )

def notify_student_of_achievement(
    db: Session,
    student_id: int,
    badge_name: str,
    badge_description: str
):
    """
    Notify student when they earn a new achievement
    
    Args:
        db: Database session
        student_id: ID of the student
        badge_name: Name of the badge earned
        badge_description: Description of the achievement
    """
    create_notification(
        db=db,
        user_id=student_id,
        type="achievement",
        title=f"🎉 Yeni Rozet: {badge_name}",
        message=badge_description,
        link="/student/dashboard"
    )

def notify_progress_milestone(
    db: Session,
    student_id: int,
    milestone_type: str,
    milestone_value: int
):
    """
    Notify student and parent of progress milestone
    
    Args:
        db: Database session
        student_id: ID of the student
        milestone_type: Type of milestone (stories, practice, speed)
        milestone_value: Value achieved
    """
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        return
    
    # Create message based on milestone type
    if milestone_type == "stories":
        title = "📚 İlerleme Kaydedildi"
        message = f"{milestone_value}. hikayeni tamamladın! Harika gidiyorsun!"
    elif milestone_type == "practice":
        title = "🔄 Pratik Başarısı"
        message = f"{milestone_value}. pratik seansını tamamladın!"
    elif milestone_type == "speed":
        title = "⚡ Hız Artışı"
        message = f"Okuma hızın {milestone_value} kelime/dakikaya ulaştı!"
    else:
        return
    
    # Notify student
    create_notification(
        db=db,
        user_id=student_id,
        type="progress",
        title=title,
        message=message,
        link="/student/dashboard"
    )
    
    # Notify parent if exists
    if student.veli_id:
        parent = db.query(User).filter(User.id == student.veli_id).first()
        if parent:
            create_notification(
                db=db,
                user_id=parent.id,
                type="progress",
                title=f"📊 {student.ad_soyad} - {title}",
                message=message,
                link="/parent/dashboard"
            )
