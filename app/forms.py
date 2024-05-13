from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, Optional, Regexp, Email, NumberRange

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

class SearchForm(FlaskForm):
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