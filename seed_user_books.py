from faker import Faker
from app import app, db, UserBook, User, Book  # Replace 'your_app' with your actual app module
import random

fake = Faker()

def seed_user_books():
    with app.app_context():  # Set up application context
        # Clear existing data
        db.session.query(UserBook).delete()
        db.session.commit()

        # Get all user and book IDs
        user_ids = [user.id for user in User.query.all()]
        book_ids = [book.id for book in Book.query.all()]
        
        if not user_ids or not book_ids:
            print("No users or books found. Please seed users and books first.")
            return

        roles = ["Owner", "Borrower"]
        user_books = []
        for _ in range(10):
            user_book = UserBook(
                user_id=random.choice(user_ids),
                book_id=random.choice(book_ids),
                role=random.choice(roles)
            )
            user_books.append(user_book)
            db.session.add(user_book)
        
        db.session.commit()
        print("Seeded 10 user-book relationships successfully.")

if __name__ == "__main__":
    seed_user_books()