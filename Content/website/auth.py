"""Import necessary modules, classes, and functions from Flask, your application, and other packages."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
# Import the database instance
from . import db
from .models import User
# Import the User model
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm
# Import the RegistrationForm class from your forms

# Create a Blueprint named 'auth'
auth = Blueprint("auth", __name__)


"""Route for user login"""
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # Query the User model to find a user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                # Log in the user
                login_user(user, remember=True)
                # Redirect to the home page
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    # Render the login template
    return render_template("login.html", user=current_user)


"""Route for user sign-up"""
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # Check if the user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to home if authenticated

    form = RegistrationForm()  # Instantiate the RegistrationForm

    if form.validate_on_submit():
        # Hash the password using SHA-256
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # Create a new user instance with the provided form data
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the changes to the database
        # Flash a success message
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))  # Redirect to the login page
    # Render the signup template
    return render_template('signup.html', form=form, user=current_user)


# Route for user logout
@auth.route("/logout")
# This decorator ensures the user is logged in before accessing the route
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for("views.home"))  # Redirect to the home page
