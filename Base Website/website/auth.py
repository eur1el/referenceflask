from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        #if user is already signed up send them straight to home page
        return redirect(url_for('home'))
    form = RegistrationForm
    if form.validate_on_submit():
        #generate hashed pssword from inputted password
        hashed_password = generate_password_hash((form.password.data), method='sha256')
        #user is composed of username from form, email from form and a hashed password generated  from the form password
        user = User(username=form.usermame.data, email =form.email.data, password = hashed_password)
        db.session.add(User)
        db.session.commit()
        flash('Your account has been created! You can now login in', 'success')
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.login'))
return render_template('signup.html', form=form, user=current_user)
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
