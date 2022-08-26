from flask import Flask, request, render_template, redirect, flash, g, session, url_for
from models import db, connect_db, User, Post, FriendList
from forms import CreateUserForm, LoginForm, PostForm, UserEditForm
from flask_login import LoginManager
from flask_mail import Message
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
import os
from seed import setup



CURR_USER_KEY = "curr_user"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bodybook'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'capstone_project'
# app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'


# configure_uploads(app, photos)


login_manager = LoginManager()
login_manager.init_app(app)

connect_db(app)
# setup()

##############################################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Log out user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup',methods=['GET','POST'])
def signup():
    """Handle user signup"""

    form = CreateUserForm()
    # if request.method == 'POST' and form.validate() == True:
    if form.validate_on_submit():
        try:
            user = User.signup(
                name = form.name.data,
                last_name = form.last_name.data,
                username = form.username.data,
                email=form.email.data,
                password=form.password.data)
            db.session.commit()
            flash('new user added')
            
            # msg = Message("Welcome to Bodybook!",sender="kendras0127@gmail.com", recipients=user.email)
            # mail.send(msg)
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/user/signup.html', form=form)
        do_login(user)
        return redirect("/login")

    else:
        return render_template('/user/signup.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():


    form = LoginForm(obj=g.user)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.authenticate(email,password)

        if user:
            do_login(user)
            flash(f'welcome back, {user.name}')
            return redirect(f"/users/{user.id}")
        else:
            form.email.errors = ['Invalid credential']

    return render_template('/user/login.html', form=form)

@app.route('/users/<int:user_id>', methods=['GET','POST'])
def feed(user_id):
    user = User.query.get_or_404(user_id)
    # all_posts = Post.query.all()
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = PostForm()
    posts = (Post.query.order_by(Post.timestamp.desc()).limit(10).all())

    if form.validate_on_submit():
        status = Post(status=form.status.data)
        g.user.posts.append(status)
        db.session.commit()

        return redirect(f'/users/{g.user.id}')

    return render_template("/user/feed.html", form=form, user=user, posts=posts)


@app.route('/users/<int:user_id>/detail')
def show_profile_page(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    form = UserEditForm()
    user = User.query.get_or_404(user_id)
    users = User.query.all()
    posts = Post.query.filter_by(author_id=user_id).all()
    friend_list = FriendList.query.filter_by(user_id=g.user.id).all()

    return render_template('/user/detail.html', user=user, friend_list=friend_list, posts=posts, form=form)


@app.route('/users/friend_request/<int:user_id>/', methods=['POST'])
def send_friend_request(user_id):
    """add new friend"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    # user = User.query.get_or_404(user_id)

    if not FriendList.query.filter_by(user_id=g.user.id, friend_of_id=user_id).first():
        db.session.add_all([
            FriendList(user_id=g.user.id, friend_of_id=user_id),
            FriendList(user_id=user_id, friend_of_id=g.user.id),
        ])
        db.session.commit()
        flash('friend request sent!')

    return redirect(f'/users/{g.user.id}/detail')


@app.route('/users/unfriend/<int:user_id>', methods=['POST'])
def unfriend(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    

    db.session.delete(FriendList.query.filter_by(user_id=g.user.id, friend_of_id=user_id).first())
    db.session.delete(FriendList.query.filter_by(user_id=user_id, friend_of_id=g.user.id).first())
    db.session.commit()
    flash('you are no longer friends with this person.')

    return redirect(f"/users/{g.user.id}/detail")


@app.route('/users/<int:user_id>/edit',methods=["GET", "POST"])
def edit_profile(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    bcrypt = Bcrypt()
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit(): 
        # filename = user.picture.save(form.photo.data)
        # file_url = url_for('get_file',filename=filename)

        user.username = form.username.data
        user.email = form.email.data
        user.password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user.country = form.country.data
        user.picture = form.picture.data

        user.bio = form.bio.data

        db.session.commit()
        flash('Profile Edited')
        return redirect(f"/users/{user.id}/detail")

    return render_template('/user/edit.html',form=form,user=user)


@app.route('/delete_account/<user_id>/', methods=['GET'])
def delete_account(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get(user_id)
    
    db.session.delete(user)
    db.session.commit()
    flash('user deleted')
    
    g.user = None
    return redirect("/")

######################################################################################################
# Handling Posts


@app.route('/status/<int:post_id>/delete', methods=['GET'])
def delete_status(post_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    status = Post.query.get(post_id)
    
    db.session.delete(status)
    db.session.commit()
    flash('post deleted')

    return redirect(f"/users/{g.user.id}")



@app.route('/logout')
def logout():
    do_logout()
    flash("You have been logged out")
    return redirect ('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

##############################################################################



##############################################################################
# Homepage

@app.route('/')
def homepage():
    form = LoginForm()
    return redirect('/signup')