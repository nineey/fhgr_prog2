from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask_paginate import Pagination, get_page_args
from flask import redirect, url_for

from libs import auth_handler
from libs.auth_handler import check_login, login_required, load_users, save_users
from libs.category_handler import load_categories
from libs.data_handler import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "ThisIsMyVerySecretKey"


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password) is True:
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route("/")
@login_required
def index():
    return render_template("index.html", deals=load_data(), user=session["USERNAME"])


@app.route("/pdp/<id>")
@login_required
def show_deal(id):
    deals = load_data()
    return render_template("detailpage.html", deal=deals[id])


@app.route("/logout")
@login_required
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for("login"))


@app.route('/new_entry', methods=['GET', 'POST'])
@login_required
def new_entry():
    if request.method == 'POST':
        deal = request.form['post_deal']
        price = request.form['post_price']
        category = request.form['post_category']
        save_data(id_handler(), deal, price, category)
        flash("Eingabe erfolgreich!")
        return redirect(url_for("new_entry"))

    return render_template("new_entry.html", categories=load_categories())


@app.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        firstname = request.form['input_firstname']
        lastname = request.form['input_firstname']
        save_users(username, password, firstname, lastname)
    return render_template("users.html", users=load_users())


@app.route("/users/delete/<username>")
@login_required
def delete_user(username):
    auth_handler.delete_user(username)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
