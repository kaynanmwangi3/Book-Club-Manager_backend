from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"))  # one-to-many
    club = db.relationship("Club", back_populates="members")

    # many-to-many with books
    user_books = db.relationship("UserBook", back_populates="user")
    books = db.relationship("Book", secondary="user_books", back_populates="users")

    serialize_rules = ("-user_books.user",  "-books.users", "-club.members", "-password_hash")

# Association table for many-to-many between Club and Book
class UserBook(db.Model, SerializerMixin):
    __tablename__ = "user_books"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    role = db.Column(db.String(50), default="owner")  # optional, e.g. "borrower", "owner"

    user = db.relationship("User", back_populates="user_books")
    book = db.relationship("Book", back_populates="user_books")

    serialize_rules = (
        "-user.user_books",   # prevent recursion into user → user_books
        "-book.user_books",   # prevent recursion into book → user_books
        "-user.books",   # cut loop user <-> books
        "-book.users",  # cut loop book <-> users
        "-user.password_hash",     # hide sensitive user field if included
    )

class Book(db.Model, SerializerMixin):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Integer)  # Rating out of 5
    reviews = db.Column(db.Text)

    # many-to-many with users
    user_books = db.relationship("UserBook", back_populates="book")
    users = db.relationship("User", secondary="user_books", back_populates="books")

    serialize_rules = ("-user_books.book", "-users.books" "-user_books.user",)

class Club(db.Model, SerializerMixin):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    meeting_date = db.Column(db.DateTime)

    # one-to-many: one club has many members
    members = db.relationship("User", back_populates="club")

    serialize_rules = ("-members.club", "-members.books", )
