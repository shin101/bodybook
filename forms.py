from re import L
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm

from models import db, User, connect_db
from wtforms_alchemy import model_form_factory, ModelForm


# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session

class CreateUserForm(FlaskForm):
    """Form for creating a new user profile"""
    name = StringField('Name', validators=[InputRequired()],render_kw={"placeholder": "First + Last Name"})
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()],render_kw={"placeholder": "Must be at least 6 characters"})

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
    picture = StringField('(Optional) Image URL')
    bio = TextAreaField('(Optional) Tell us about yourself')


class PostForm(FlaskForm):
    status = TextAreaField("What's on your mind?")

# class LoginForm(ModelForm):
#     class Meta:
#         model = User
