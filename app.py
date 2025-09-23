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
