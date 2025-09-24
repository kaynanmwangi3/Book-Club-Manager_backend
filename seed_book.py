from faker import Faker
from app import app, db
from models import Book, User, Club
import random

fake = Faker()

def seed_books(n=15):
    with app.app_context():
        # Get existing users and clubs
        users = User.query.all()
        clubs = Club.query.all()
        
        if not users:
            print("No users found. Please seed users first.")
            return
        
        # Clear old book data
        Book.query.delete()
        
        books = []
        genres = ['Fiction', 'Non-Fiction', 'Mystery', 'Romance', 'Sci-Fi', 'Fantasy', 'Biography', 'History']
        
        for _ in range(n):
            title = fake.catch_phrase()
            author = fake.name()
            description = fake.text(max_nb_chars=200)
            publish_year = fake.year()
            genre = random.choice(genres)
            rating = random.randint(1, 5)
            reviews = fake.text(max_nb_chars=150)
            member_id = random.choice(users).id if users else None
            club_id = random.choice(clubs).id if clubs else None

            book = Book(
                title=title,
                author=author,
                description=description,
                publish_year=publish_year,
                genre=genre,
                rating=rating,
                reviews=reviews,
                member_id=member_id,
                club_id=club_id
            )
            books.append(book)

        db.session.add_all(books)
        db.session.commit()
        print(f" Seeded {n} books successfully!")

if __name__ == "__main__":
    seed_books()