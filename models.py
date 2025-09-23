from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    books = db.relationship("Book", back_populates="owner", cascade="all, delete-orphan")
    club_memberships = db.relationship("BookClub", back_populates="member", cascade="all, delete-orphan")
    serialize_rules = ("-books.owner", "-club_memberships.member")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    rating = db.Column(db.Integer) # Rating out of 5
    reviews = db.Column(db.Text)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"))

    owner = db.relationship("User", back_populates="books")
    club = db.relationship("Club", back_populates="books")
    serialize_rules = ("-owner.books", "-club.books")


class Club(db.Model, SerializerMixin):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    meeting_date = db.Column(db.DateTime)

    books = db.relationship("Book", back_populates="club", cascade="all, delete-orphan")
    memberships = db.relationship("BookClub", back_populates="club", cascade="all, delete-orphan")
    serialize_rules = ("-books.club", "-memberships.club")


class BookClub(db.Model, SerializerMixin):
    __tablename__ = "book_clubs"

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String, nullable=False, default="member")

    club = db.relationship("Club", back_populates="memberships")
    member = db.relationship("User", back_populates="club_memberships")
    serialize_rules = ("-club.memberships", "-member.club_memberships") 

