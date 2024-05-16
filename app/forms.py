"""
This module declares all the forms used by the flask application
"""
from app import db
from app.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField#, FileRequired
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length,\
    Email, EqualTo, AnyOf, ValidationError, Regexp, NumberRange
import sqlalchemy as sa

STATES = ['NSW','QLD','TAS','VIC','WA','ACT','NT']

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address"), Length(max=128)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64)])
    confirmed_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    # address fields
    address_line1 = StringField('Address Line 1', validators=[DataRequired(), Length(min=2, max=64)])
    address_line2 = StringField('Address Line 2', validators=[Length(max=64)])
    suburb = StringField('Suburb', validators=[DataRequired(), Length(max=32)])
    postcode = StringField('Post Code', validators=[DataRequired(), Length(min=4,max=4,message="Post code must be 4 digits"), Regexp('[0-9]{4}',message="Post code must only contain digits")])
    city = StringField('City', validators=[DataRequired(), Length(max=32)])
    state = SelectField('State', choices=(['STATE'] + STATES), validators=[DataRequired(), AnyOf(STATES, "Please pick a state"), Length(max=32)])
    #country = StringField('Country', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Create Account')

    # Derived from flask mega tutorial
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address')

class LoginForm(FlaskForm):
    """
    Login Form used to allow users to login
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UploadForm(FlaskForm):
    """
    Upload Form used to allow users to upload posts to the website
    """
    post_type = SelectField('Post Type', choices=[('OFFER','Give'),('REQUEST','Request')])
    item_name = StringField('Item Name', validators=[DataRequired(), Length(max=32)])
    desc = TextAreaField('Description', validators=[DataRequired(), Length(max=256)])
    image = FileField('Image File')#, validators=[FileRequired()])

    submit = SubmitField('Post')

class ContactForm(FlaskForm):
    """
    Contact Form used to allow users to contact the creators of the website
    """
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired(),\
                    Email("This field requires a valid email address")])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class SearchForm(FlaskForm):
    """
    Search Form used to allow users to search posts on the website
    """
    q = StringField('Title')
    md = IntegerField('Max Distance (km)', validators=[NumberRange(min=0, max=25)])
    order = SelectField('Order By', choices=
        [
            ('',        'Select'),
            ('close',   'Closest'),
            ('new',     'Newest'),
            ('old',     'Oldest'),
            ('rating',  'Vendor Rating')
        ])
