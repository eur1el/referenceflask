

import os
from pathlib import Path
from PIL import Image 
import secrets 
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from .forms import RegistrationForm, UpdateAccountForm, PostForm
from . import db
from website import create_app
from PIL import Image
from flask import current_app
from secrets import token_hex

"""profane words"""
profane_words = ["shit", "fuck", "cunt",]


"""Create a Blueprint named 'views'"""
views = Blueprint("views", __name__)




"""home page route"""
@views.route("/")
@views.route("/home")
def home():
    """home page route"""
    page = Post.query.all()  # This seems unnecessary. 'page' variable is defined but not used.
    return render_template("home.html", user=current_user, posts=posts)


"""home page route"""
@views.route("/")
@views.route("/about")
def aboutme():
    """home page route"""
    page = Post.query.all()  # Same as above, 'page' is not used.
    return render_template("aboutme.html", user=current_user, posts=posts)


# Contact page route
@views.route("/")
@views.route("/contact")
def contact():
    """home page route"""
    page = Post.query.all()  # Same as above, 'page' is not used.
    return render_template("contact.html", user=current_user, posts=posts)


# Terms page route
@views.route("/")
@views.route("/terms")
def terms():
    page = Post.query.all()  # Same as above, 'page' is not used.
    return render_template("terms.html", user=current_user, posts=posts)


# Privacy page route
@views.route("/")
@views.route("/privacy")
def privacy():
    page = Post.query.all()  # Same as above, 'page' is not used.
    return render_template("privacy.html", user=current_user, posts=posts)


# Blog page route
@views.route("/blog")
@login_required
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("blog.html", user=current_user, posts=posts)


# Tutorials page route
@views.route("/tutorials")
@login_required
def tutorials():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("tutorials.html", user=current_user, posts=posts)


# Create post route
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        post = Post(title=title, text=text, author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', category='success')
        return redirect(url_for('views.blog'))


    return render_template('create_post.html', form=form, user=current_user)


# Delete post route
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif post.author!= current_user.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.blog'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.blog'))

    posts = Post.query.filter_by(user=user).order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
         # Profanity filter
        for word in profane_words:
            if re.search(rf'\b{re.escape(word)}\b', text, re.I):
                flash('Your comment contains inappropriate language.', category='error')
                return redirect(url_for('views.blog'))
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.blog'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.blog'))

#view/route for likes on posts
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

#allows for saving pictures for account profile pictures
def save_picture(form_picture):
    # Get the path to the profile pictures directory
    path = Path(current_app.root_path) / 'static' / 'profile_pics'

    # Generate a random filename using tokens
    random_hex = random_tokenhex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    # Set the full path for saving the image
    picture_path = path / picture_fn

    # Resize the image to a desired output size
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save the resized image to the specified path
    i.save(picture_path)

    # Return the filename for the saved image
    return picture_fn
    
#view/route for account updates, updates user profile picture
@views.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated!')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', user=current_user, image_file=image_file, form=form)




"""Create update post route"""
@views.route("/update-post/<id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.author != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Your Post has been Updated!', category='success')
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
        return render_template("blog.html", user=current_user, posts=posts)
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('update_post.html', form=form, user=current_user, post=post, image_file=image_file)
