from flask import Flask, render_template, flash
import plotly.graph_objects as go
import plotly
from libs.auth_handler import *
from libs.category_handler import *
from libs.data_handler import *

app = Flask(__name__)
# secret key for session based stuff like login and flash. should be more secret in real project.
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


@app.route("/all/<page>")
@login_required
def all_deals_range(page):
    count = 10
    page_int = int(page)
    page_int_for_data = page_int - 1
    start = page_int_for_data * count
    max_pages = int(load_data_range(start, count)[1])
    # add some restrictions to prevent url manipulation
    if int(page) > max_pages:
        start = 0
        return redirect(url_for("all_deals_range", page=1))
    elif int(page) < 1:
        return redirect(url_for("all_deals_range", page=1))
    else:
        return render_template("all.html", deals=load_data_range(start, count)[0], user=session["USERNAME"],
                               nextPage=page_int + 1, prevPage=page_int - 1, max_pages=max_pages, page=int(page))


@app.route("/pdp/<id>")
@login_required
def show_deal(id):
    deals = load_data()
    labels = ['Accepted', 'Rejected']
    colors = ['green', 'red']
    values = [get_voting(id)[2], get_voting(id)[3]]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors))
    plotly_div = plotly.io.to_html(fig, include_plotlyjs=True, full_html=False)
    return render_template("detailpage.html", deal=deals[id], accepted=get_voting(id)[0], rejected=get_voting(id)[1],
                           accepted_counter=get_voting(id)[2], rejected_counter=get_voting(id)[3],
                           voting_pie=plotly_div)


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
        if check_price(price) is False:
            flash("Please enter a number for price (int or float)", "danger")
            return redirect(url_for("new_entry"))
        else:
            save_data(id_handler(), deal, price, category)
            flash("New deal successfully added!", "success")
            return redirect(url_for("new_entry"))
    return render_template("new_entry.html", categories=load_categories())


@app.route('/categories')
@login_required
def categories():
    return render_template("categories.html", categories=load_categories())


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        category = request.form['post_category']
        if check_category(category) is False:
            flash("Category already exists. Please try again.", "warning")
            return redirect(url_for("categories"))
        else:
            save_category(category)
            flash("Category successfully added!", "success")
            return redirect(url_for("categories"))


@app.route('/category/delete/<category>')
@login_required
def categories_delete_category(category):
    delete_category(category)
    return redirect(url_for("categories"))


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


@app.route("/stats")
@login_required
def stats():
    return render_template("stats.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
