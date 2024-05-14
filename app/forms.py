"""
This module declares all the forms used by the flask application
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField#, FileRequired
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange

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
    desc = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
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
            ('',        ''),
            ('close',   'Closest'),
            ('new',     'Newest'),
            ('old',     'Oldest'),
            ('rating',  'Vendor Rating')
        ])
