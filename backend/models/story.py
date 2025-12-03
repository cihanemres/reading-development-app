from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    sinif_duzeyi = Column(Integer, nullable=False, index=True)  # 2, 3, or 4
    baslik = Column(String(255), nullable=False)
    metin = Column(Text, nullable=False)
    kapak_gorseli = Column(String(500), nullable=True)  # Path to cover image
    ses_dosyasi = Column(String(500), nullable=True)  # Path to MP3 file
    kelime_sayisi = Column(Integer, nullable=True)  # Auto-calculated word count
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    quiz_questions = relationship("QuizQuestion", back_populates="story", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Story {self.baslik} (Grade {self.sinif_duzeyi})>"
