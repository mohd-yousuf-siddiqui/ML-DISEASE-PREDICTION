import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Create extensions
db = SQLAlchemy(model_class=Base)
mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# Register template test
@app.template_test('search')
def search_test(value, pattern):
    """Test if a string matches a pattern (case-insensitive)."""
    import re
    if isinstance(value, str):
        return bool(re.search(pattern, value, re.IGNORECASE))
    return False

# Configure SqlAlchemy
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'disease_prediction.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/disease_prediction")

# Configure Flask-Login
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize extensions
db.init_app(app)
mongo.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Create database tables
with app.app_context():
    # Import models
    import models  # noqa: F401
    db.create_all()

    # Create admin user if not exists
    from models import User
    try:
        admin = User.query.filter_by(username=os.environ.get('ADMIN_USERNAME', 'admin')).first()
        if not admin:
            admin_user = User(
                username=os.environ.get('ADMIN_USERNAME', 'admin'),
                email=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
                is_admin=True
            )
            admin_user.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin_user)
            db.session.commit()
            logging.info("Admin user created successfully")
    except Exception as e:
        logging.error(f"Error creating admin user: {str(e)}")
        db.session.rollback()

# Import routes after app is created to avoid circular imports
from routes import *

# Initialize ML models when the application starts
with app.app_context():
    from routes import initialize
    initialize()
