from sqlalchemy import create_engine, text
import os
import sys

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://okuma_user:ygeYNt3325NhEHCieYeRcbhgEGsMnuB3@dpg-d4pd1jq4i8rc73cn0640-a.frankfurt-postgres.render.com/okuma_db_o2bl")

def run_single_migration(engine, description, sql):
    """Run a single migration command in its own transaction"""
    print(f"  → {description}...")
    try:
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
        print(f"    ✓ Success")
        return True
    except Exception as e:
        if "already exists" in str(e) or "duplicate" in str(e).lower():
            print(f"    ○ Already exists (skipped)")
        else:
            print(f"    ✗ Error: {e}")
        return False

def run_migration():
    print("🔄 Starting database migration...")
    print(f"   Database: {DATABASE_URL[:50]}...")
    
    engine = create_engine(DATABASE_URL)
    
    migrations = [
        ("Add 'ders' column to stories", 
         "ALTER TABLE stories ADD COLUMN IF NOT EXISTS ders VARCHAR(100)"),
        
        ("Add 'konu_ozeti' column to stories", 
         "ALTER TABLE stories ADD COLUMN IF NOT EXISTS konu_ozeti TEXT"),
        
        ("Add 'sorular' column to stories", 
         "ALTER TABLE stories ADD COLUMN IF NOT EXISTS sorular TEXT"),
        
        ("Add 'answers_json' column to answers", 
         "ALTER TABLE answers ADD COLUMN IF NOT EXISTS answers_json TEXT"),
        
        ("Add 'teacher_id' column to users", 
         "ALTER TABLE users ADD COLUMN IF NOT EXISTS teacher_id INTEGER REFERENCES users(id)"),
        
        ("Add 'is_approved' column to users", 
         "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_approved BOOLEAN DEFAULT FALSE"),
        
        ("Create assignments table",
         """CREATE TABLE IF NOT EXISTS assignments (
             id SERIAL PRIMARY KEY,
             teacher_id INTEGER NOT NULL REFERENCES users(id),
             student_id INTEGER NOT NULL REFERENCES users(id),
             story_id INTEGER NOT NULL REFERENCES stories(id),
             status VARCHAR(50) DEFAULT 'bekliyor',
             assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
             due_date TIMESTAMP WITH TIME ZONE,
             completed_at TIMESTAMP WITH TIME ZONE
         )"""),
        
        ("Set existing users as approved",
         "UPDATE users SET is_approved = TRUE WHERE is_approved IS NULL"),
    ]
    
    success_count = 0
    for description, sql in migrations:
        if run_single_migration(engine, description, sql):
            success_count += 1
    
    print(f"✅ Migration completed: {success_count}/{len(migrations)} successful")

if __name__ == "__main__":
    run_migration()

