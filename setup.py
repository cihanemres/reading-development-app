"""
Test script to verify database connection and create initial admin user
"""
import sys
sys.path.append('backend')

from sqlalchemy import text
from backend.database import SessionLocal, init_db
from backend.models.user import User, UserRole
from backend.auth.password import hash_password

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure PostgreSQL is running and database 'okuma_db' exists.")
        print("   Create it with: CREATE DATABASE okuma_db;")
        return False

def create_tables():
    """Create all database tables"""
    print("\n🔨 Creating database tables...")
    try:
        init_db()
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def create_admin_user():
    """Create initial admin user"""
    print("\n👤 Creating admin user...")
    try:
        db = SessionLocal()
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@okuma.com").first()
        if existing_admin:
            print("ℹ️  Admin user already exists!")
            db.close()
            return True
        
        # Create admin
        admin = User(
            ad_soyad="Yönetici",
            email="admin@okuma.com",
            password_hash=hash_password("admin123"),
            rol=UserRole.ADMIN
        )
        
        db.add(admin)
        db.commit()
        db.close()
        
        print("✅ Admin user created!")
        print("   Email: admin@okuma.com")
        print("   Password: admin123")
        return True
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

def create_sample_users():
    """Create sample users for testing"""
    print("\n👥 Creating sample users...")
    try:
        db = SessionLocal()
        
        # Sample teacher
        if not db.query(User).filter(User.email == "ogretmen@test.com").first():
            teacher = User(
                ad_soyad="Ayşe Öğretmen",
                email="ogretmen@test.com",
                password_hash=hash_password("ogretmen123"),
                rol=UserRole.OGRETMEN
            )
            db.add(teacher)
        
        # Sample students
        students_data = [
            ("Ahmet Yılmaz", "ahmet@test.com", 2),
            ("Zeynep Demir", "zeynep@test.com", 3),
            ("Mehmet Kaya", "mehmet@test.com", 4),
        ]
        
        for name, email, grade in students_data:
            if not db.query(User).filter(User.email == email).first():
                student = User(
                    ad_soyad=name,
                    email=email,
                    password_hash=hash_password("ogrenci123"),
                    rol=UserRole.OGRENCI,
                    sinif_duzeyi=grade
                )
                db.add(student)
        
        # Sample parent
        if not db.query(User).filter(User.email == "veli@test.com").first():
            parent = User(
                ad_soyad="Fatma Veli",
                email="veli@test.com",
                password_hash=hash_password("veli123"),
                rol=UserRole.VELI
            )
            db.add(parent)
        
        db.commit()
        db.close()
        
        print("✅ Sample users created!")
        print("\n📋 Test Accounts:")
        print("   Admin: admin@okuma.com / admin123")
        print("   Teacher: ogretmen@test.com / ogretmen123")
        print("   Student (2nd): ahmet@test.com / ogrenci123")
        print("   Student (3rd): zeynep@test.com / ogrenci123")
        print("   Student (4th): mehmet@test.com / ogrenci123")
        print("   Parent: veli@test.com / veli123")
        return True
    except Exception as e:
        print(f"❌ Failed to create sample users: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 OKUMA GELİŞTİRME UYGULAMASI - KURULUM")
    print("=" * 60)
    
    # Test database connection
    if not test_database_connection():
        return
    
    # Create tables
    if not create_tables():
        return
    
    # Create admin user
    if not create_admin_user():
        return
    
    # Create sample users
    create_sample_users()
    
    print("\n" + "=" * 60)
    print("✅ KURULUM TAMAMLANDI!")
    print("=" * 60)
    print("\n📝 Sonraki Adımlar:")
    print("1. Backend'i başlat:")
    print("   cd backend")
    print("   python -m uvicorn main:app --reload")
    print("\n2. Frontend'i başlat (yeni terminal):")
    print("   cd frontend")
    print("   python -m http.server 3000")
    print("\n3. Tarayıcıda aç:")
    print("   http://localhost:3000")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
