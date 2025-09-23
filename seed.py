from faker import Faker
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app, db
from models import User

fake = Faker()

def seed_users(n=10):
    with app.app_context():
        # Clear old data
        User.query.delete()
        
        users = []
        for _ in range(n):
            name = fake.name()
            email = fake.unique.email()
            phone_number = fake.unique.msisdn()[:10]  # Generates a 10-digit number
            password_hash = generate_password_hash("password123")  # Default password for all users

            user = User(
                name=name,
                email=email,
                password_hash=password_hash,
                phone_number=phone_number,
                join_date=datetime.utcnow()
            )
            users.append(user)

        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Seeded {n} users successfully!")

if __name__ == "__main__":
    seed_users()
