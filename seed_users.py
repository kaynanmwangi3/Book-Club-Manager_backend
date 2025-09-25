from faker import Faker
from datetime import datetime
from app import app, db, User, Club  # Replace 'your_app' with your actual app module
from werkzeug.security import generate_password_hash
import random

fake = Faker()

def seed_users():
    with app.app_context():  # Set up application context
        # Clear existing data
        db.session.query(User).delete()
        db.session.commit()

        # Get all club IDs
        club_ids = [club.id for club in Club.query.all()]
        if not club_ids:
            print("No clubs found. Please seed clubs first.")
            return

        users = []
        for _ in range(10):
            user = User(
                name=fake.name(),
                email=fake.unique.email(),
                password_hash=generate_password_hash("password123"),  # Hashing the fixed password
                phone_number=fake.unique.phone_number(),
                join_date=fake.date_time_this_year(),
                club_id=random.choice(club_ids) if club_ids else None
            )
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print("Seeded 10 users successfully.")

if __name__ == "__main__":
    seed_users()