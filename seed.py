from curses.ascii import FF
import requests
from models import FriendList, db, User, Post


def setup():
    db.drop_all()
    db.create_all()

    users = []
    for i in range(0,2):
        res = requests.get('https://randomuser.me/api/')
        data = res.json()['results'][0]
        users.append(User(name=data['name']['first'],last_name=data['name']['last'], username=data['login']['username'],password=data['login']['password'], picture=data['picture']['thumbnail'], big_pic=data['picture']['large'], gender=data['gender'],country=data['location']['country'],email=data['email']))

    db.session.add_all(users)
    db.session.commit()

    post1 = Post(status='Feeling hungry',author_id=users[0].id)
    post2 = Post(status='Bored',author_id=users[1].id)
    posts = [post1, post2]

    db.session.add_all(posts)
    db.session.commit()
