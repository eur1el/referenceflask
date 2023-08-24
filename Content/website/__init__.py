# Import necessary modules and classes from Flask and SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Define the name of the database file
DB_NAME = "database.db"

# Function to create the Flask application
def create_app():
    # Create a Flask app instance
    app = Flask(__name__)

    # Configure the app's secret key for session security
    app.config['SECRET_KEY'] = "eurieljaidenbeltransveryveryverysecretkey1234"
    
    # Configure the app's database URI to connect to SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize the SQLAlchemy database with the app
    db.init_app(app)

    # Import views and auth blueprints
    from .views import views
    from .auth import auth
    
    # Register the blueprints with the app and define their URL prefixes
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import models for database
    from .models import User, Post, Comment, Like

    # Create the database tables if they do not exist
    with app.app_context():
        db.create_all()
        print("Created database!")

    # Create a LoginManager instance for handling user authentication
    login_manager = LoginManager()
    
    # Set the view to redirect to for unauthorized users
    login_manager.login_view = "auth.login"
    
    # Initialize the LoginManager with the app
    login_manager.init_app(app)

    # Define a user loader function for the LoginManager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app  # Return the created Flask app instance
