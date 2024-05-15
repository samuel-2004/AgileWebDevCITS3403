from flask import render_template, send_from_directory, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from json import loads
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlparse, parse_qs
import sqlalchemy as sa
from app import db
from app.blueprints import main
from app.models import *
from app.forms import *
from werkzeug.utils import secure_filename
import newhome

#Since we are using os, avoid importing as much as possible
import os
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

@main.route('/', methods=['GET'])
@main.route('/index')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts, defaultimage='book.jpg')

@main.route('/advancedsearch')
def advancedSearch():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form["q"]
        max_distance = request.form["md"]
        orderby = request.form["order"]
        print({'title': title, 'max_distance': max_distance, 'orderby': orderby})
        return redirect(url_for('main.search', q=title, md=max_distance, order=orderby))
    else:
        return render_template('advancedsearch.html', form=form)

@main.route('/search')
def search():
    # Retrieve search parameters from the query string
    query = request.args.get('q')
    max_distance = request.args.get('md')
    orderby = request.args.get('order')

    posts = get_posts(query, max_distance, orderby)
    return render_template('search.html', posts=posts, defaultimage='book.jpg', form=SearchForm())

@main.route('/account')
def account():
    return render_template('account.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET','POST'])
@main.route('/contact-us', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        print({'name': name, 'email': email, 'subject': subject, 'message': message})
        return redirect(url_for('main.contact'))
    else:
        return render_template('contact.html', form=form)

@main.route('/item/<int:itemID>')
def item(itemID):
    return render_template('items.html', itemID=itemID)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = uploadForm()
    if form.validate_on_submit():
        post = Post(post_type = form.post_type.data, item_name = form.item_name.data, 
                    desc = form.desc.data, author=current_user)
        db.session.add(post)
        #db.session.commit()
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            new_name = str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + '_'+ filename
            path = '/static/data/photos/' + new_name
            image.save(os_join(basedir + '/static/data/photos/',new_name))
            
            image = Image(src = path, post = post)
            db.session.add(image)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)

@main.route('/user')
@login_required
def user():
    username = request.args.get('username')
    user = db.first_or_404(sa.select(User).where(User.username == username))
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.session.scalars(query)
    #posts = [
    #    {'author': user, 'item_name': 'Test post #1'},
    #    {'author': user, 'item_name': 'Test post #2'}
    #]
    return render_template('user.html', user=user, posts=posts)
'''
# Try the main directory if a file is not found in the root branch
@main.route('/<path:filename>')
def get_file(filename):
    # Check if the file exists in the original directory
    original_path = os_join(main.static_folder, filename)
    if os_pathexists(original_path):
        return send_from_directory(main.static_folder, filename)
    
    # If not found, try to locate the file in the directory of the Flask app
    app_directory_path = os_dirname(os_abspath(__file__))
    app_file_path = os_join(app_directory_path, filename)
    if os_pathexists(app_file_path):
        return send_from_directory(app_directory_path, filename)

    # If the file is not found in either location, return a 404 error
    return "File not found", 404
'''
