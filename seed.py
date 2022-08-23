from curses.ascii import FF
import requests
from models import db, User, Post


def setup():
    db.drop_all()
    db.create_all()

    users = []
    for i in range(0,2):
        res = requests.get('https://randomuser.me/api/')
        data = res.json()['results'][0]
        users.append(User(name=data['name']['first'], username=data['login']['username'],password=data['login']['password'], picture=data['picture']['thumbnail'], gender=data['gender'],country=data['location']['country'],email=data['email']))

    post1 = Post(status='Feeling hungry')
    post2 = Post(status='Bored')


    db.session.add_all(users, [post1,post2])
    db.session.commit()
