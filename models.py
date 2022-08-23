# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from wtforms_alchemy import ModelForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# engine = create_engine('sqlite:///:memory:')
# Base = declarative_base(engine)
# Session = sessionmaker(bind=engine)
# session = Session()


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# WTForms-Alchemy
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    username = db.Column(db.Text)
    picture = db.Column(db.Text, default="/static/images/default-pic.png")
    gender = db.Column(db.Text)
    country = db.Column(db.Text)
    email = db.Column(db.Text,nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False)
    posts = db.relationship('Post')

    @classmethod
    def signup(cls, name, username,email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(name=name, username=username, email=email, password=hashed_pwd)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls,email,password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(500),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'),nullable=False)





# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     picture = db.Column(db.Text, default="/static/images/default-pic.png")
#     gender = db.Column(db.Text)
#     country = db.Column(db.Text)

#     @classmethod
#     def signup(cls, username, password):
#         """Sign up user.

#         Hashes password and adds user to system.
#         """
#         hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

         