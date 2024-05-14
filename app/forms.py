from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address"), Length(max=128)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password', "Passwrods must match")])
    # address fields
    address_line1 = StringField('Address Line 1', validators=[DataRequired(), Length(min=2, max=64)])
    address_line2 = StringField('Address Line 2', validators=[Length(max=64)])
    suburb = StringField('Suburb', validators=[DataRequired(), Length(max=32)])
    postcode = StringField('Post Code', validators=[DataRequired(), Length(min=4,max=4,message="Post code must be 4 digits")])
    city = StringField('City', validators=[DataRequired(), Length(max=32)])
    state = SelectField('State', choices=['STATE','NSW','QLD','TAS','VIC','WA','ACT','NT'], validators=[DataRequired(), Length(max=32)])
    #country = StringField('Country', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class uploadForm(FlaskForm):
    post_type = SelectField('Post Type', choices=[('OFFER','Give'),('REQUEST','Request')])
    item_name = StringField('Item Name', validators=[DataRequired(), Length(max=32)])
    desc = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
    image = FileField('Image File')#, validators=[FileRequired()])

    submit = SubmitField('Post')
    
class ContactForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address")])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')