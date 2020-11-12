import functools
import json
#source: https://www.programcreek.com/python/example/58659/werkzeug.security.check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
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

    password = generate_password_hash(password)
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
    if check_password_hash(user["password"], password):
        session["USERNAME"] = user["username"]
        return True
    else:
        print("password incorrect")
        return redirect(request.url)


def save_user(users):
    with open('data/users.json', 'w') as db:
        json.dump(users, db, indent=4)


def delete_user(username):
    users = load_users()
    del users[username]
    save_user(users)
