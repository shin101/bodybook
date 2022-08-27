from flask_bcrypt import Bcrypt
from curses.ascii import FF
import requests
from models import FriendList, db, User, Post


def setup():
    db.drop_all()
    db.create_all()

    bcrypt = Bcrypt()

    users = []
    for i in range(0,3):
        res = requests.get('https://randomuser.me/api/')
        data = res.json()['results'][0]
        users.append(User(name=data['name']['first'],last_name=data['name']['last'], username=data['login']['username'],password=bcrypt.generate_password_hash(data['login']['password']).decode('UTF-8'), picture=data['picture']['thumbnail'], big_pic=data['picture']['large'], gender=data['gender'],country=data['location']['country'],email=data['email']))

    db.session.add_all(users)
    db.session.commit()

    post1 = Post(status='Feeling hungry',author_id=users[0].id)
    post2 = Post(status='Bored',author_id=users[1].id)
    post3 = Post(status='Who wants to hang out?',author_id=users[1].id)
    posts = [post1, post2, post3]

    db.session.add_all(posts)
    db.session.commit()
