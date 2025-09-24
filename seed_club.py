from faker import Faker
from datetime import datetime
from app import app, db, Club  # Replace 'your_app' with your actual app module

fake = Faker()

def seed_clubs():
    with app.app_context():  # Set up application context
        # Clear existing data
        db.session.query(Club).delete()
        db.session.commit()

        clubs = []
        for _ in range(10):
            club = Club(
                name=fake.company() + " Book Club",
                description=fake.paragraph(nb_sentences=3),
                meeting_date=fake.date_time_between(start_date="now", end_date="+1y")
            )
            clubs.append(club)
            db.session.add(club)
        
        db.session.commit()
        print("Seeded 10 clubs successfully.")

if __name__ == "__main__":
    seed_clubs()