from re import L
from wtforms import StringField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm
# from flask_uploads import UploadSet, IMAGES, configure_uploads

from models import db, User, connect_db
# from wtforms_alchemy import model_form_factory, ModelForm

# photos = UploadSet('photos',IMAGES)

# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session

class CreateUserForm(FlaskForm):
    """Form for creating a new user profile"""
    name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=6)])

class PostForm(FlaskForm):
    """Form for adding or editing posts"""
    text = TextAreaField('text', validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email',validators=[InputRequired()])
    password = PasswordField('Password',validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for adding users"""
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    # picture = FileField('(Optional) Image URL',validators=[FileAllowed(photos, 'Only images are allowed')])
    picture = StringField('(Optional) Image URL')
    country = StringField('(Optional) Country')
    bio = TextAreaField('(Optional) Tell us about yourself')
    


class PostForm(FlaskForm):
    status = TextAreaField("What's on your mind?")

# class LoginForm(ModelForm):
#     class Meta:
#         model = User
