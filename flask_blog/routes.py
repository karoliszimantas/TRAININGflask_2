from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateForm, PostForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {0}!".format(form.username.data))
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print(request.args)
            return redirect(url_for('home'))
        else:
            flash("login unsuccessful")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_text = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_text
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    picture.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.image_file = picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect("account")
    elif request.method == "GET":
        form.username.data = current_user.username
        form.username.data = current_user.username
    image_file = url_for("static", filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New post", form=form)

