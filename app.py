from flask import Flask, render_template, flash

from libs.auth_handler import *
from libs.category_handler import *
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
        else:
            flash("Incorrect username or password. Please try again.", "warning")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        firstname = request.form['input_firstname']
        lastname = request.form['input_lastname']
        if check_username(username) == "taken":
            flash("Username already taken. Please try again.", "danger")
            redirect(url_for("register"))
        else:
            save_new_user(username, password, firstname, lastname)
            flash("Successfully registered. Enter your login below.", "success")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/")
@login_required
def index():
    return render_template("voting.html", deals=load_data(), user=session["USERNAME"])


@app.route("/all")
@login_required
def all_deals():
    return render_template("all.html", deals=load_data(), user=session["USERNAME"])


@app.route("/all/<page>")
@login_required
def all_deals_range(page):
    count = 10
    page_int = int(page)
    page_int_for_data = page_int - 1
    start = page_int_for_data * count
    return render_template("all.html", deals=load_data_range(start, count), user=session["USERNAME"], nextPage=page_int+1, prevPage=page_int-1)


@app.route("/pdp/<id>")
@login_required
def show_deal(id):
    deals = load_data()
    return render_template("detailpage.html", deal=deals[id])


@app.route("/voting/<vote>/<deal_id>")
@login_required
def voting_vote(deal_id, vote):
    username = session["USERNAME"]
    add_voting(deal_id, username, vote)
    return redirect(url_for("index"))


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
        flash("New deal successfully added!")
        return redirect(url_for("new_entry"))

    return render_template("new_entry.html", categories=load_categories())


@app.route('/new_entry/new_category', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        category = request.form['post_category']
        save_category(category)
        flash("Category successfully added!")
        return redirect(url_for("new_entry"))


@app.route("/users")
@login_required
def users():
    return render_template("users.html", users=load_users())


@app.route("/users/add", methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        firstname = request.form['input_firstname']
        lastname = request.form['input_lastname']
        if check_username(username) == "taken":
            flash("Username already taken. Please try again.")
            redirect(url_for("users"))
        else:
            save_new_user(username, password, firstname, lastname)
            return redirect(url_for("users"))
    return render_template("users.html", users=load_users())


@app.route("/users/delete/<username>")
@login_required
def users_delete_user(username):
    delete_user(username)
    return redirect(url_for("users"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
