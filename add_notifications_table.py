"""
Database migration to create notifications table
"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def create_notifications_table():
    """Create notifications table with indexes"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        
        cursor = conn.cursor()
        
        # Create notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                link VARCHAR(255),
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notifications_user_id 
            ON notifications(user_id);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notifications_is_read 
            ON notifications(is_read);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notifications_created_at 
            ON notifications(created_at DESC);
        """)
        
        conn.commit()
        print("✅ Notifications table created successfully!")
        print("✅ Indexes created successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating notifications table: {e}")
        raise

if __name__ == "__main__":
    create_notifications_table()
