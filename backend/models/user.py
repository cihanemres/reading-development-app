from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from database import Base

class UserRole(str, enum.Enum):
    STUDENT = "ogrenci"
    TEACHER = "ogretmen"
    PARENT = "veli"
    ADMIN = "yonetici"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ad_soyad = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(SQLEnum(UserRole), nullable=False)
    sinif_duzeyi = Column(Integer, nullable=True)  # Only for students (2, 3, or 4)
    parent_id = Column(Integer, nullable=True)  # For linking student to parent
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.email} ({self.rol})>"
