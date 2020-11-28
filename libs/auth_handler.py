"""
Contains everything related to login and user handling.
"""

import functools
import json
#source: https://www.programcreek.com/python/example/58659/werkzeug.security.check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for, request


def login_required(func):
    """
    function to handle access to protected pages.
    Add "@login_required" to app_route for protection
    source: https://blog.tecladocode.com/protecting-endpoints-in-flask-apps-by-requiring-login/
    """
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "USERNAME" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return secure_function


def check_login(username, password):
    """
    function checks the user inputs for login and sets the session
    :param username: user input for username
    :param password: user input for password
    :return: "True", if login is correct / redirect to login page, if login wrong
    """
    users = load_users()

    # check if given username exists
    if username.lower() not in users:
        # return to login page
        return redirect(request.url)
    else:
        user = users[username.lower()]
    # check if given password matches the username
    # if true: set session
    # re-hash password to check the input
    if check_password_hash(user["password"], password):
        session["USERNAME"] = user["username"]
        return True
    else:
        # redirect to login page if password wrong
        return redirect(request.url)



# get users
def load_users():
    """
    function loads users from JSON-File
    :return: dictionary with all user data
    """
    with open('data/users.json', 'r') as db:
        users = json.load(db)
    return users


def save_user(users):
    """
    saves the user list (dict) into JSON-File
    :param users: dictionary of all users
    """
    with open('data/users.json', 'w') as db:
        json.dump(users, db, indent=4)


def delete_user(username):
    """
    function to delete a user form the user list
    Not possible to delete the admin user
    :param username: unique main key of dict to identify which user to delete
    """
    users = load_users()
    del users[username.lower()]
    save_user(users)


def save_new_user(username, password, firstname, lastname):

    try:
        with open('data/users.json', 'r') as db:
            users = json.load(db)
    except:
        users = {}

    # hash password for security reasons
    password = generate_password_hash(password)
    users[username.lower()] = {"username": username, "password": password, "firstname": firstname.capitalize(), "lastname": lastname.capitalize()}

    with open('data/users.json', 'w') as db:
        json.dump(users, db, indent=4)


def check_username(username):
    users = load_users()
    if username.lower() in users.keys():
        return "taken"
    else:
        pass



