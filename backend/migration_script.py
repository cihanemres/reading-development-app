from sqlalchemy import create_engine, text
import os
import sys

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get DATABASE_URL
DATABASE_URL = "postgresql://okuma_user:ygeYNt3325NhEHCieYeRcbhgEGsMnuB3@dpg-d4pd1jq4i8rc73cn0640-a.frankfurt-postgres.render.com/okuma_db_o2bl"

def run_migration():
    print("Connecting to database...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        print("Adding 'ders' column...")
        try:
            connection.execute(text("ALTER TABLE stories ADD COLUMN ders VARCHAR(100)"))
            print("Success.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        print("Adding 'konu_ozeti' column...")
        try:
            connection.execute(text("ALTER TABLE stories ADD COLUMN konu_ozeti TEXT"))
            print("Success.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        print("Adding 'sorular' column...")
        try:
            connection.execute(text("ALTER TABLE stories ADD COLUMN sorular TEXT"))
            print("Success.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        print("Adding 'answers_json' column to 'answers' table...")
        try:
            connection.execute(text("ALTER TABLE answers ADD COLUMN answers_json TEXT"))
            print("Success.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        print("Adding 'teacher_id' column to 'users' table...")
        try:
            connection.execute(text("ALTER TABLE users ADD COLUMN teacher_id INTEGER REFERENCES users(id)"))
            print("Success.")
        except Exception as e:
            print(f"Skipped (maybe exists): {e}")

        connection.commit()
    
    print("Migration completed.")

if __name__ == "__main__":
    run_migration()
