from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import get_db
from models.user import User, UserRole
from auth.password import hash_password, verify_password
from auth.jwt_handler import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Pydantic schemas
class RegisterRequest(BaseModel):
    ad_soyad: str
    email: EmailStr
    password: str
    rol: UserRole
    sinif_duzeyi: Optional[int] = None
    parent_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    ad_soyad: str
    email: str
    rol: UserRole
    sinif_duzeyi: Optional[int]
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate grade level for students
    if request.rol == UserRole.STUDENT:
        if not request.sinif_duzeyi or request.sinif_duzeyi not in [2, 3, 4]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Students must have a valid grade level (2, 3, or 4)"
            )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create new user
    new_user = User(
        ad_soyad=request.ad_soyad,
        email=request.email,
        password_hash=password_hash,
        rol=request.rol,
        sinif_duzeyi=request.sinif_duzeyi,
        parent_id=request.parent_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    token_data = {
        "user_id": new_user.id,
        "email": new_user.email,
        "rol": new_user.rol.value
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "ad_soyad": new_user.ad_soyad,
            "email": new_user.email,
            "rol": new_user.rol.value,
            "sinif_duzeyi": new_user.sinif_duzeyi
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and return JWT token
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "rol": user.rol.value
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "ad_soyad": user.ad_soyad,
            "email": user.email,
            "rol": user.rol.value,
            "sinif_duzeyi": user.sinif_duzeyi
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(lambda: __import__('backend.auth.dependencies', fromlist=['get_current_user']).get_current_user)
):
    """
    Get current user information
    """
    return current_user

class UpdateProfileRequest(BaseModel):
    ad_soyad: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: __import__('backend.auth.dependencies', fromlist=['get_current_user']).get_current_user)
):
    """
    Update current user's profile
    """
    # Update name if provided
    if request.ad_soyad:
        current_user.ad_soyad = request.ad_soyad
    
    # Update email if provided and not already taken
    if request.email and request.email != current_user.email:
        existing = db.query(User).filter(User.email == request.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = request.email
    
    # Update password if provided
    if request.password:
        current_user.password_hash = hash_password(request.password)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
