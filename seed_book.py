from faker import Faker
from app import app, db, Book  # Replace 'your_app' with your actual app module
import random

fake = Faker()

def seed_books():
    with app.app_context():  # Set up application context
        # Clear existing data
        db.session.query(Book).delete()
        db.session.commit()

        books = []
        genres = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Romance", "Thriller"]
        for _ in range(10):
            book = Book(
                title=fake.catch_phrase(),
                author=fake.name(),
                description=fake.paragraph(nb_sentences=5),
                publish_year=fake.year(),
                genre=random.choice(genres),
                rating=random.randint(1, 5),
                reviews=fake.paragraph(nb_sentences=3)
            )
            books.append(book)
            db.session.add(book)
        
        db.session.commit()
        print("Seeded 10 books successfully.")

if __name__ == "__main__":
    seed_books()