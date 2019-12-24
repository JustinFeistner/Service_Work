import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from servicework import app, db, bcrypt
from servicework.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from servicework.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    """If the user is logged in, they will be redirected to their current posts. If
    the user is not logged in, they will be invited to login or register."""
    return render_template('home.html', title='Home')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """This invokes the RegistrationForm in forms.py and checks all its validators when the user
    clicks the submit button. If the validators pass, the user is added 
    to the db and is redirected to the login screen. If the validators fail, the template
    shows the user error messages."""
    form = RegistrationForm()
    print(f"Form: {form}")
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        print(f"User: {user}")
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """This invokes the LoginForm in forms.py and checks all its validators when the user
    clicks the submit button. If the validators pass, the user's password is verified, 
    the user is logged in, and redirected to the home page. If validators fail, the 
    template shows the user error messages."""
    form = LoginForm()
    print(f"Form: {form}")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #password_match_check = bcrypt.check_password_hash(user.password, form.password.data)
        print(f"User: {user}")
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print(f"Entered password matches user password? {bcrypt.check_password_hash(user.password, form.password.data)}")
            login_user(user, remember=form.remember.data)
            return redirect(url_for('user_posts', username=current_user.username))
        else:
            #print(f"Entered password matches user password? {bcrypt.check_password_hash(user.password, form.password.data)}")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    """This calls on a logout_user function in the flask_login module that logs the 
    current_user out."""
    logout_user()
    return redirect(url_for('home'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """The user has to be logged in to make account changes. This invokes the 
    UpdateAccountForm in forms.py and checks all its validators when the user clicks 
    the submit button. If validators pass, user can enter a new username and/or 
    password and this will be saved to the DB when they click submit. """
    form = UpdateAccountForm()
    print(f"Form: {form}")
    if form.validate_on_submit():
        current_user.username = form.username.data
        print(f"Updated user username: {current_user.username}")
        current_user.email = form.email.data
        print(f"Updated user email: {current_user.email}")
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_posts', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        print(f"Current user username: {form.username.data}")
        form.email.data = current_user.email
        print(f"Current user email: {form.email.data}")
    return render_template('account.html', title='Account', form=form)
                     


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """This allows a logged in user to create a post. This invokes the 
    PostForm in forms.py and checks all its validators when the user clicks 
    the submit button. Valid data is then sent to the DB. If validators fail, 
    the user sees an error message."""
    form = PostForm()
    print(f"Form: {form}")
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user_posts', username=current_user.username))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    """This allows the user to select a single post. This is used for updating
    and deleting a post."""
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """This makes sure the user cant manually switch to somebody elses posts. Then, if all
    the fields on the form are filled out correctly, it updates the post."""
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('user_posts', username=current_user.username))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('create_post.html', title='Update Weight', form=form, legend='Update Weight')
                           

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """This makes sure the user cant manually switch to somebody elses posts. Then, the post
    is deleted."""
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('user_posts', username=current_user.username))


@app.route("/user/<string:username>")
def user_posts(username):
    """This allows users that are logged in to see all their posts in ascending order."""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.asc())\
        .paginate(page=page, per_page=5)
    postsDesc = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())
    # If the user hasn't made any posts, this catches the "NoneType" error and gives our variables values
    try:
        firstWeight = int(posts.query.first().content)
        mostRecentWeight = int(postsDesc.first().content)
    except AttributeError:
        firstWeight = 0
        mostRecentWeight = 0
    # This tells the user how much weight they have gained or lost. 
    if (mostRecentWeight - firstWeight) > 0:
        weightChange = f"You have gained {mostRecentWeight - firstWeight} lb since you started using this app."
    elif (mostRecentWeight - firstWeight) < 0:
        weightChange = f"You have lost {firstWeight - mostRecentWeight} lb since you started using this app."
    else:
        weightChange = f"You have not lost or gained weight."

    return render_template('user_posts.html', posts=posts, weightChange=weightChange, user=user)