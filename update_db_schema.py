import sys
sys.path.insert(0, 'C:/Users/cihanemres/Desktop/proj/backend')

from sqlalchemy import text
from database import engine, SessionLocal
from models.reading_activity import Answer
from models.quiz import QuizQuestion

def add_column_if_not_exists():
    with engine.connect() as conn:
        try:
            # Try to select the column to see if it exists
            conn.execute(text("SELECT dogru_sayisi FROM answers LIMIT 1"))
            print("✅ Column 'dogru_sayisi' already exists.")
        except Exception:
            print("⚠️ Column 'dogru_sayisi' does not exist. Adding it...")
            # Add column
            try:
                conn.execute(text("ALTER TABLE answers ADD COLUMN dogru_sayisi INTEGER"))
                conn.commit()
                print("✅ Column added successfully.")
            except Exception as e:
                print(f"❌ Error adding column: {e}")

def update_scores():
    db = SessionLocal()
    try:
        answers = db.query(Answer).all()
        print(f"Found {len(answers)} answers to update.")
        
        for answer in answers:
            # Get questions for this story
            questions = db.query(QuizQuestion).filter(
                QuizQuestion.story_id == answer.story_id
            ).order_by(QuizQuestion.id).all()
            
            correct_count = 0
            student_answers = [answer.q1, answer.q2, answer.q3, answer.q4]
            
            for i, q in enumerate(questions):
                if i < 4:
                    if student_answers[i] == q.correct_answer:
                        correct_count += 1
            
            answer.dogru_sayisi = correct_count
            print(f"Updated Answer ID {answer.id}: Score = {correct_count}")
            
        db.commit()
        print("✅ All scores updated successfully.")
    except Exception as e:
        print(f"❌ Error updating scores: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_column_if_not_exists()
    update_scores()
