"""
Contains everything related to login and user handling.
"""

import functools
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for, request
import os

# source: https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'))


def login_required(func):
    """
    Handle access to protected pages.
    Add "@login_required" to app_route for protection
    Source: https://blog.tecladocode.com/protecting-endpoints-in-flask-apps-by-requiring-login/
    """

    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "USERNAME" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return secure_function


def check_login(username, password):
    """
    Check the entered login credentials and set username into the session
    :param username: User input for username
    :param password: User input for password
    :return: "True", if login is correct / redirect to login page, if login wrong
    Source: https://www.programcreek.com/python/example/58659/werkzeug.security.check_password_hash
    """
    users = load_users()

    # check if given username exists
    if username.lower() not in users or users[username.lower()]["status"] == "disabled":
        # return to login page
        return redirect(request.url)
    else:
        user = users[username.lower()]
    # check status of the user
    # check if given password matches the username
    # if true: set session
    # re-hash password to check the input
    if check_password_hash(user["password"], password):
        session["USERNAME"] = user["username"].lower()
        return True
    else:
        # redirect to login page if password wrong
        return redirect(request.url)


def load_users():
    """
    function loads users from JSON-File
    :return: dictionary with all user data
    """
    with open(DATA_PATH, 'r') as db:
        users = json.load(db)
    return users


def save_user(users):
    """
    saves the user list (dict) into JSON-File
    :param users: dictionary of all users
    """
    with open(DATA_PATH, 'w') as db:
        json.dump(users, db, indent=4)


def delete_user(username):
    """
    function to delete a user form the user list
    in order to keep the votings, user will be deactivated but not removed in users.json
    Not possible to deactivate the admin user
    :param username: unique main key of dict to identify which user to deactivate
    """
    users = load_users()
    users[username.lower()]["status"] = "disabled"
    save_user(users)


def save_new_user(username, password, firstname, lastname):
    """
    Save a user to new or existing JSON-file
    Hash the password before saving.
    Source: https://www.programcreek.com/python/example/58659/werkzeug.security.check_password_hash
    """
    try:
        with open(DATA_PATH, 'r') as db:
            users = json.load(db)
    except:
        users = {}

    # hash password for security reasons
    password = generate_password_hash(password)
    users[username.lower()] = {"username": username.lower(), "password": password, "firstname":
        firstname.capitalize(), "lastname": lastname.capitalize(), "status": "enabled"}

    with open(DATA_PATH, 'w') as db:
        json.dump(users, db, indent=4)


def check_username(username):
    """
    Check if username is already taken.
    :param username: Username which was entered in the form
    :return: String "taken" if username is taken, otherwise do nothing
    """
    users = load_users()
    if username.lower() in users.keys():
        return "taken"
    else:
        pass
