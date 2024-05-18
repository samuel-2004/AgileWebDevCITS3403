"""
This module defines all the routes for the website
"""

from os.path import join as os_join, dirname as os_dirname, \
     abspath as os_abspath
from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa

from app import db
from app.blueprints import main
from werkzeug.utils import secure_filename
from app.models import User, Post, Image, Address, Reply
from app.forms import LoginForm, UploadForm, ContactForm, SearchForm, SignupForm
from app.controllers import get_posts, calc_time_ago

@main.route('/', methods=['GET'])
@main.route('/index')
def index():
    """
    The home page for the website
    """
    posts = get_posts()
    return render_template('index.html', page="index", posts=posts, calcTimeAgo=calc_time_ago)

@main.route('/advancedsearch')
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
        return redirect(url_for('main.search', q=title, md=max_distance, order=orderby))
    else:
        return render_template('advancedsearch.html', form=form)

@main.route('/search')
def search():
    """
    A search page that displays results
    """
    # Retrieve search parameters from the query string
    query = request.args.get('q')
    max_distance = request.args.get('md')
    orderby = request.args.get('order')
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    posts = get_posts(query, max_distance, orderby, lat, lng)
    return render_template('search.html', page="search", posts=posts, form=SearchForm(), calcTimeAgo=calc_time_ago)


@main.route('/about')
def about():
    """
    A page to describe the website and show what it's about
    """
    return render_template('about.html')

@main.route('/contact', methods=['GET','POST'])
@main.route('/contact-us', methods=['GET','POST'])
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
        return redirect(url_for('main.contact'))
    else:
        return render_template('contact.html', form=form)

@main.route('/post/<int:post_id>')
def post(post_id):
    """
    A page for each post
    """
    # Fetch the post with the given postID
    post = Post.query.get(post_id)
    return render_template('items.html', post=post)

@main.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    The login page
    """
    # redirect if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login_page'))
        login_user(user, remember=form.remember_me.data)
        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    The signup page
    """
    # redirect if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # form
    form = SignupForm()
    if form.validate_on_submit():
        # add address
        address = Address(address_line1=form.address_line1.data, address_line2=form.address_line2.data)
        address.suburb = form.suburb.data
        address.postcode = form.postcode.data
        address.city = form.city.data
        address.state = form.state.data
        address.latitude = form.lat.data
        address.longitude = form.lng.data
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
        return redirect(url_for('main.login_page'))
    # render page
    return render_template('signup.html', active_link='/signup', form=form)

@main.route('/logout')
def logout():
    """
    Users will logout and be redirected to the home page
    """
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/upload', methods=['GET', 'POST'])
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
        current_user.points += 1
        if post.post_type == "OFFER":
            current_user.given += 1
        elif post.post_type == "REQUEST":
            current_user.requested += 1
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
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)

@main.route('/user')
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
    return render_template('user.html', page="user", user=user, posts=posts, calcTimeAgo=calc_time_ago, is_user_page=True)

@main.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = db.session.get(Post,post_id)
    if post.author == current_user:
        current_user.points -= 1
        if post.post_type == "OFFER":
            current_user.given -= 1
        elif post.post_type == "REQUEST":
            current_user.requested -= 1
        image = post.images
        if image:
            db.session.delete(image)
        query = post.replies.select()
        replies = db.session.scalars(query)
        for reply in replies:
            db.session.delete(reply)
        db.session.delete(post)
        db.session.commit()
        flash(f"Post {post.item_name} deleted")
    else:
        flash(f"Only {post.author.username} can delete their own post!")
    return redirect(url_for('main.index'))
