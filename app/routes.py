"""
This module defines all the routes for the website
"""

from os.path import join as os_join, dirname as os_dirname, \
     exists as os_pathexists, abspath as os_abspath
from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, send_from_directory, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.utils import secure_filename
from app import flaskApp, db
from app.models import User, Post, Image, get_posts
from app.forms import LoginForm, UploadForm, ContactForm, SearchForm

@flaskApp.route('/', methods=['GET'])
@flaskApp.route('/index')
def index():
    """
    The home page for the website
    """
    posts = get_posts()
    return render_template('index.html', posts=posts, defaultimage='book.jpg')

@flaskApp.route('/advancedsearch')
def advanced_search():
    """
    A search page
    """
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form["q"]
        max_distance = request.form["md"]
        orderby = request.form["order"]
        print({'title': title, 'max_distance': max_distance, 'orderby': orderby})
        return redirect(url_for('search', q=title, md=max_distance, order=orderby))
    else:
        return render_template('advancedsearch.html', form=form)

@flaskApp.route('/search')
def search():
    """
    A search page that displays results
    """
    # Retrieve search parameters from the query string
    query = request.args.get('q')
    max_distance = request.args.get('md')
    orderby = request.args.get('order')

    posts = get_posts(query, max_distance, orderby)
    return render_template('search.html', posts=posts, defaultimage='book.jpg', form=SearchForm())

@flaskApp.route('/account')
def account():
    """
    A page to show a user's account details
    """
    return render_template('account.html')

@flaskApp.route('/about')
def about():
    """
    A page to describe the website and show what it's about
    """
    return render_template('about.html')

@flaskApp.route('/contact', methods=['GET','POST'])
@flaskApp.route('/contact-us', methods=['GET','POST'])
def contact():
    """
    A page to contact the developers
    Currently the method only prints to terminal.
    In the future, we would hope that it would send an automatic email to
        a helpdesk email such as contact-us@example.com
    """
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        print({'name': name, 'email': email, 'subject': subject, 'message': message})
        return redirect(url_for('contact'))
    else:
        return render_template('contact.html', form=form)

@flaskApp.route('/item/<int:itemID>')
def item(itemID):
    """
    A page for each item
    """
    return render_template('items.html', itemID=itemID)

@flaskApp.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    The login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@flaskApp.route('/signup')
def signup():
    """
    The signup page
    """
    return render_template('signup.html')

@flaskApp.route('/logout')
def logout():
    """
    Users will logout and be redirected to the home page
    """
    logout_user()
    return redirect(url_for('index'))

@flaskApp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Users can upload new posts here
    They must be logged in to do so
    """
    form = UploadForm()
    if form.validate_on_submit():
        post = Post(post_type = form.post_type.data, item_name = form.item_name.data,
                    desc = form.desc.data, author=current_user)
        db.session.add(post)
        #db.session.commit()
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            basedir = os_abspath(os_dirname(__file__))
            new_name = str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + '_'+ filename
            path = '/static/data/photos/' + new_name
            image.save(os_join(basedir + '/static/data/photos/',new_name))

            image = Image(src = path, post = post)
            db.session.add(image)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)

@flaskApp.route('/user')
@login_required
def user():
    """
    Users can access their user account
    They must be logged in
    """
    username = request.args.get('username')
    user = db.first_or_404(sa.select(User).where(User.username == username))
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.session.scalars(query)
    #posts = [
    #    {'author': user, 'item_name': 'Test post #1'},
    #    {'author': user, 'item_name': 'Test post #2'}
    #]
    return render_template('user.html', user=user, posts=posts)

# Try the main directory if a file is not found in the root branch
@flaskApp.route('/<path:filename>')
def get_file(filename):
    """
    If the path for a file cannot be found, try the 
    """
    # Check if the file exists in the original directory
    original_path = os_join(flaskApp.static_folder, filename)
    if os_pathexists(original_path):
        return send_from_directory(flaskApp.static_folder, filename)

    # If not found, try to locate the file in the directory of the Flask app
    app_directory_path = os_dirname(os_abspath(__file__))
    app_file_path = os_join(app_directory_path, filename)
    if os_pathexists(app_file_path):
        return send_from_directory(app_directory_path, filename)

    # If the file is not found in either location, return a 404 error
    return "File not found", 404
