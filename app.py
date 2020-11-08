from flask import Flask
from flask import render_template
from flask import request
from flask import session, redirect, url_for
from libs.data_handler import *
from functools import wraps
from flask import g

app = Flask(__name__)
# app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"

"""
@app.before_request
def check_session():
    if not session.get("USERNAME") is None:
        g.users = load_users()
        username = session.get("USERNAME")
        g.user = g.users[username]
    return redirect(url_for("new_entry"))


"""


@app.route("/")
def index():
    return render_template("index.html", deals=load_data())


@app.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":

        req = request.form

        username = req.get("username")
        password = req.get("password")

        if not username in g.users:
            print("Username not found")
            return redirect(request.url)
        else:
            user = g.users[username]

        if not password == user["password"]:
            print("Incorrect password")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            print("session username set")
            return redirect(url_for("index"))

    return render_template("sign-in.html")


@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)

    return redirect(url_for("sign_in"))


@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        deal = request.form['post_deal']
        price = request.form['post_price']
        save_data(id_handler(), deal, price)
        return render_template("new_entry.html", message="Danke für deine Eingabe!")

    return render_template("new_entry.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
