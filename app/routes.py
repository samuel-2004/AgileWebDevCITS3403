from flask import render_template, send_from_directory, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from json import loads
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlparse, parse_qs
import sqlalchemy as sa
from app import flaskApp, db
from app.models import *
from app.forms import *
from werkzeug.utils import secure_filename
import newhome

#Since we are using os, avoid importing as much as possible
import os
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

@flaskApp.route('/', methods=['GET'])
@flaskApp.route('/index')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts, defaultimage='book.jpg')

@flaskApp.route('/advancedsearch')
def advancedSearch():
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
    # Retrieve search parameters from the query string
    query = request.args.get('q')
    max_distance = request.args.get('md')
    orderby = request.args.get('order')

    posts = get_posts(query, max_distance, orderby)
    return render_template('search.html', posts=posts, defaultimage='book.jpg', form=SearchForm())

@flaskApp.route('/account')
def account():
    return render_template('account.html')

@flaskApp.route('/about')
def about():
    return render_template('about.html')

@flaskApp.route('/contact', methods=['GET','POST'])
@flaskApp.route('/contact-us', methods=['GET','POST'])
def contact():
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
    # Fetch the post with the given itemID
    post = Post.query.get(itemID)
    return render_template('items.html', post=post)


@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    # redirect if logged in
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

@flaskApp.route('/signup', methods=['GET', 'POST'])
def signup():
    # redirect if logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form
    form = SignupForm()
    if form.validate_on_submit():
        # add address
        address = Address(address_line1=form.address_line1.data, address_line2=form.address_line2.data)
        address.suburb = form.suburb.data
        address.postcode = form.postcode.data
        address.city = form.city.data
        address.state = form.state.data
        address.country = "Australia"           # All accounts are registered in Australia for now
        db.session.add(address)
        db.session.commit()
        # add user
        user = User(username=form.username.data)
        user.email = form.email.data
        user.set_password(form.password.data)
        user.bio = "I'm using NewHome"          # default
        user.pic = "default_profile_pic.png"    # default
        user.address_id = address.id
        db.session.add(user)
        db.session.commit()
        # submit and redirect
        flash("Congratulations! Welcome to NewHome!")
        return redirect(url_for('login'))
    # render page
    return render_template('signup.html', active_link='/signup', form=form)

@flaskApp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@flaskApp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = uploadForm()
    if form.validate_on_submit():
        post = Post(post_type = form.post_type.data, item_name = form.item_name.data, 
                    desc = form.desc.data, author=current_user)
        db.session.add(post)
        current_user.points += 1
        if post.post_type == "OFFER":
            current_user.given += 1
        elif post.post_type == "REQUEST":
            current_user.requested += 1
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
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)

@flaskApp.route('/user')
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

# Try the main directory if a file is not found in the root branch
@flaskApp.route('/<path:filename>')
def get_file(filename):
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
