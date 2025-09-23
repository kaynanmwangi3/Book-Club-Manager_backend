from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Book, Club 
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
    return jsonify({"success": True, "user": user.to_dict(only=('name','email','phone_number'))}), 200

@app.route('/users', methods=["GET"])
def get_users():
    Users = User.query.all()

    if Users:
        return jsonify({"success":True, "users": [user.to_dict(only=('name','email','phone_number')) for user in Users]}), 200
    return jsonify({"success": False, "message": "No users found"}), 404

@app.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({"success": True, "user": user.to_dict(only=('name','email','phone_number'))}), 200
    return jsonify({"success": False, "message": "User not found"}), 404

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"success":False, "message":"User not found"}), 404

    data = request.get_json()

    new_name = data.get('name')
    if new_name != user.name:
        existing_user = User.query.filter_by(name=new_name).first()
        # If there exists a user with this name, AND that user is NOT me
        if existing_user and existing_user.id != user.id:
            return jsonify({"success":False, "message":"Name already taken"}), 409
        user.name = new_name
     
    new_email = data.get('email')
    if new_email != user.email:
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"success":False, "message":"Email already taken"}), 409
        user.email = new_email

    new_phone_number = data.get('phone_number')
    if new_phone_number != user.phone_number:
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
        member_id=data.get('member_id'),
        club_id=data.get('club_id')
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Book added successfully", "book": book.to_dict()}), 201
 