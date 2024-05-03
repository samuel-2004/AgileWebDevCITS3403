from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, Optional, Regexp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class uploadForm(FlaskForm):
    post_type = SelectField('Post Type', choices=[('OFFER','Give'),('REQUEST','Request')])
    item_name = StringField('Item Name', validators=[DataRequired(), Length(max=32)])
    desc = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
    image = FileField('Image File', validators=[FileRequired()])

    submit = SubmitField('Post')