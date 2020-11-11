import functools
import json
from flask import session, redirect, url_for, request

# source: https://blog.tecladocode.com/protecting-endpoints-in-flask-apps-by-requiring-login/
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "USERNAME" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return secure_function

# get users
def load_users():
    with open('data/users.json', 'r') as db:
        users = json.load(db)
    return users


def save_users(username, password, firstname, lastname):
    try:
        with open('data/users.json', 'r') as db:
            users = json.load(db)
    except:
        users = {}

    users[username] = {"username": username, "password": password, "firstname": firstname, "lastname": lastname}

    with open('data/users.json', 'w') as db:
        json.dump(users, db, indent=4)


def check_login(username, password):
    users = load_users()

    if username not in users:
        print("username not found")
        return redirect(request.url)
    else:
        user = users[username]
    if not password == user["password"]:
        print("password incorrect")
        return redirect(request.url)
    else:
        session["USERNAME"] = user["username"]
        print(session)
        return True





