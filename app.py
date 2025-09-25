from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Book, Club, UserBook
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


@app.route('/signup', methods=["POST"])
def signup():
    data = request.get_json()
    name= data.get('name')
    email = data.get('email') 
    password = data.get('password')
    phone_number = data.get('phone_number')
    join_date = datetime.utcnow()

    if not (name and email and password and phone_number):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter((User.name == name) | (User.email== email) | (User.phone_number == phone_number)).first():
        return jsonify({"error": "User with this name, email or phone number already exists"}), 400

    hashed_password = generate_password_hash(password)
    user = User(name=name, email=email, password_hash=hashed_password, phone_number=phone_number, join_date=join_date)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": f"User {name} created successfully"}), 201

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not (name and password):
        return jsonify({"message":" Missing required fields"}), 400

    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Invalid name or password"}), 401
    return jsonify({"success": True, "user": user.to_dict(only=('name','email','phone_number','id'))}), 200

@app.route('/users', methods=["GET"])
def get_users():
    Users = User.query.all()

    if Users:
        return jsonify({"success":True, "users": [user.to_dict() for user in Users]}), 200
    return jsonify({"success": False, "message": "No users found"}), 404

@app.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({"success": True, "user": user.to_dict()}), 200
    return jsonify({"success": False, "message": "User not found"}), 404

@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"success":False, "message":"User not found"}), 404

    data = request.get_json()

    new_name = data.get('name')
    if new_name is not None and new_name != user.name:
        existing_user = User.query.filter_by(name=new_name).first()
        # If there exists a user with this name, AND that user is NOT me
        if existing_user and existing_user.id != user.id:
            return jsonify({"success":False, "message":"Name already taken"}), 409
        user.name = new_name
     
    new_email = data.get('email')
    if new_email is not None and new_email != user.email:
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"success":False, "message":"Email already taken"}), 409
        user.email = new_email

    new_phone_number = data.get('phone_number')
    if new_phone_number is not None and new_phone_number != user.phone_number:
        existing_user = User.query.filter_by(phone_number=new_phone_number).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"success":False, "message":"Phone number already taken"}), 409
        user.phone_number = new_phone_number

    new_password = data.get("password")
    if new_password:
        user.password_hash = generate_password_hash(new_password)

    try:
        db.session.commit()
        return jsonify ({"success":True, "user":f"User {user.name} updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success":False, "message":"An error occurred while updating the user"}), 500

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"success":False, "message":"User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"sucess":True, "message":f"User {user.name} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success":False, "message":"An error occurred while deleting the user"}), 500

# Book routes
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify({"success": True, "books": [book.to_dict() for book in books]}), 200

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404
    return jsonify({"success": True, "book": book.to_dict()}), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    
    title = data.get('title')
    author = data.get('author')
    
    if not (title and author):
        return jsonify({"error": "Title and author are required"}), 400
    
    book = Book(
        title=title,
        author=author,
        description=data.get('description'),
        publish_year=data.get('publish_year'),
        genre=data.get('genre'),
        rating=data.get('rating'),
        reviews=data.get('reviews'),
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Book added successfully", "book": book.to_dict()}), 201
 
@app.route('/books/<int:id>', methods=['PATCH'])
def update_book(id):
    book = Book.query.get(id)
    
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'description' in data:
        book.description = data['description']
    if 'publish_year' in data:
        book.publish_year = data['publish_year']
    if 'genre' in data:
        book.genre = data['genre']
    if 'rating' in data:
        book.rating = data['rating']
    if 'reviews' in data:
        book.reviews = data['reviews']
    if 'member_id' in data:
        book.member_id = data['member_id']
    
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Book updated successfully", "book": book.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred while updating the book"}), 500

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"success": True, "message": "Book deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred while deleting the book"}), 500

@app.route('/clubs', methods=["GET"])
def get_clubs():
    clubs = Club.query.all()
    if clubs:
        return jsonify({"success":True, "clubs": [club.to_dict() for club in clubs]}), 200
    return jsonify({"success": False, "message": "No clubs found"}), 404

@app.route('/clubs/<int:id>', methods=["GET"])
def get_club(id):
    club = Club.query.filter_by(id=id).first()
    if club:
        return jsonify({"success":True, "club": club.to_dict()}), 200
    return jsonify({"success": False, "message": "Club not found"}), 404

@app.route('/clubs', methods=["POST"])
def add_club():
    club = request.get_json()
    name = club.get('name')
    description = club.get('description')
    meeting_date_str = club.get('meeting_date')

    if not (name and description):
        return jsonify({"error": "Missing required fields"}), 400

        if Club.query.filter((name == club.name)).first():
            return jsonify({"error": "Book Club with this name already exists"}), 400

    meeting_date = datetime.strptime(meeting_date_str, '%Y-%m-%d %H:%M:%S') 
        
    new_club = Club(name=name, description=description, meeting_date=meeting_date)
    db.session.add(new_club)
    db.session.commit()
    return jsonify({"success":True, "message": f" Book Club {name} created successfully"}), 201

@app.route('/clubs/<int:id>', methods=['PATCH'])
def update_club(id):
    club = Club.query.get(id)

    if not club:
        return jsonify({"success":False, "message":"Club not found"}), 404

    data = request.get_json()

    new_name = data.get('name')
    if new_name is not None and new_name != club.name:
        existing_club = Club.query.filter_by(name=new_name).first()
        # If there exists a club with this name, AND that club is NOT me
        if existing_club and existing_club.id != club.id:
            return jsonify({"success":False, "message":"Name already taken"}), 409
        club.name = new_name
     
    new_description = data.get('description')
    if new_description:
        club.description = new_description

    new_meeting_date_str = data.get("meeting_date")
    if new_meeting_date_str:
        try:
            new_meeting_date = datetime.strptime(new_meeting_date_str, '%Y-%m-%d %H:%M:%S')
            club.meeting_date = new_meeting_date
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

    try:
        db.session.commit()
        return jsonify ({"success":True, "club":f"Club {club.name} updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success":False, "message":"An error occurred while updating the club"}), 500

@app.route('/clubs/<int:id>', methods=['DELETE'])
def delete_club(id):
    club = Club.query.get(id)

    if not club:
        return jsonify({"success":False, "message":"Club not found"}), 404
    try:
        db.session.delete(club)
        db.session.commit()
        return jsonify({"sucess":True, "message":f"Club {club.name} deleted successfully"}), 200
    except Exeption as e:
        db.session.rollback()
        return jsonify({"success":False, "message":"An error occurred while deleting the club"}), 500

@app.route('/books/ownership/<int:book_id>/', methods=['POST'])
def add_member_to_club(book_id):
    data = request.get_json()
    user_id = data.get('user_id')
    role = data.get('role')

    if not user_id:
        return jsonify({"success": False, "message": "User ID is required"}), 400

    book = UserBook.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    existing_ownership = UserBook.query.filter_by(book_id=book_id, user_id=user_id).first()
    if existing_ownership:
        return jsonify({"success": False, "message": "User is already has this book"}), 409

    ownership = UserBook(book_id=book_id, user_id=user_id, role=role)
    db.session.add(ownership)
    db.session.commit()

    return jsonify({"success": True}), 201

if __name__ == '__main__':
    app.run(debug=True)