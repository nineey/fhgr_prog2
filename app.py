from flask import Flask, render_template, flash
import plotly.graph_objects as go
import plotly
from libs.auth_handler import *
from libs.category_handler import *
from libs.data_handler import *

app = Flask("Votery")
# secret key for session based stuff like login and flash. should be more secret in real project.
app.config["SECRET_KEY"] = "1234ThisIsTheVerySecretKeyOfNineey4321"


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Show the login page and check user login.
    :return: First, template "login.html".
            If given login is valid it redirects to voting page.
    """
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password) is True:
            return redirect(url_for('index'))
        else:
            flash("Username oder Passwort ist falsch. Bitte nochmals probieren.", "warning")
    return render_template("login.html", title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Part of the login page. User can register himself for the service.
    :return: Template "login.html"
    """
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        firstname = request.form['input_firstname']
        lastname = request.form['input_lastname']
        if check_username(username) == "taken":
            flash("Der Username ist bereits vergeben.", "danger")
            redirect(url_for("register"))
        else:
            save_new_user(username, password, firstname, lastname)
            flash("Erfolgreich registriert! Du kannst dich jetzt einloggen.", "success")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """
    Start of the application after login
    :return: Load template "voting.html"
    """
    return render_template("voting.html", title="Voting", deals=load_data(), user=session["USERNAME"], categories=load_categories())


@app.route("/all/<page>")
@login_required
def all_deals_range(page):
    """
    Show all deals in a list with pagination
    :param page: Number of the current page (10 entries per page)
    :return: Load template "all.html" with paginated list of all deals
    """
    count = 10
    page_int = int(page)
    # page = 1 is index = 0
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
        return render_template("all.html", title="Overview", deals=load_data_range(start, count)[0], user=session["USERNAME"],
                               nextPage=page_int + 1, prevPage=page_int - 1, max_pages=max_pages, page=int(page))


@app.route('/delete/<deal_id>', methods=['GET', 'POST'])
@login_required
def delete_entry(deal_id):
    """
    Allow to delete a deal.
    :param deal_id: identification of the deal
    :return: redirect to referred page
    """
    delete_entry_byID(deal_id)
    return redirect(request.referrer)


@app.route("/pdp/<id>")
@login_required
def show_deal(id):
    """
    Show the detailpage of a chosen deal.
    :param id: Identification number of the deal
    :return: Load template "detailpage.html" with deal data
    """
    if check_key(id) is False:
        return render_template("404.html")
    else:
        deals = load_data()
        labels = ['Accepted', 'Rejected']
        colors = ['green', 'red']
        values = [get_voting(id)[2], get_voting(id)[3]]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors))
        plotly_div = plotly.io.to_html(fig, include_plotlyjs=True, full_html=False)
        # get_voting(id)[X] --> [0]:list_accepted, [1]list_rejected, [2]list_accepted_length, [3]list_rejected_length
        return render_template("detailpage.html", title="Details", deal=deals[id], deal_id=id, users=load_users(), categories=load_categories(),
                            accepted=get_voting(id)[0], rejected=get_voting(id)[1],
                            accepted_counter=get_voting(id)[2], rejected_counter=get_voting(id)[3],
                            voting_pie=plotly_div)


@app.route("/voting/<vote>/<deal_id>")
@login_required
def voting_vote(deal_id, vote):
    """
    Allows the user to vote for the deal.
    :param deal_id: identifier for the deal
    :param vote: accept / reject
    :return: redirects to referred page
    """
    username = session["USERNAME"]
    add_voting(deal_id, username, vote)
    return redirect(request.referrer)


@app.route("/logout")
@login_required
def logout():
    """
    Logout function. Removes the username from session.
    :return: Redirects to login page.
    """
    session.pop("USERNAME", None)
    return redirect(url_for("login"))


@app.route('/new_entry', methods=['GET', 'POST'])
@login_required
def new_entry():
    """
    Function to save a new deal (product) into data.json
    :return: first, render Template "new_entry.html".
            After adding a new deal or error, redirect to the same page but with flash message in session
    """
    if request.method == 'POST':
        name = request.form['post_name']
        producer = request.form['post_producer']
        new_price = request.form['post_price_new']
        old_price = request.form['post_price_old']
        category = request.form['post_category']
        link = request.form['post_link']
        # check price: new price must be smaller than old price
        if check_price(new_price, old_price) is False:
            flash("Der Aktionspreis muss kleiner als der Stattpreis sein!", "danger")
            return redirect(url_for("new_entry"))
        else:
            save_new_deal(id_handler(), name, producer, new_price, old_price, link, category)
            flash("Neuer Deal hinzugefügt!", "success")
            return redirect(url_for("new_entry"))
    return render_template("new_entry.html", title="Neuer Eintrag", categories=load_categories())


@app.route('/update_deal/<id>', methods=['GET', 'POST'])
@login_required
def update_deal(id):
    """
    Allows to edit the data of a deal in the database
    :param id: unique identifier of the deal, which is to update
    :return: redirect to previous detailpage
    """
    if request.method == 'POST':
        name = request.form['post_name']
        producer = request.form['post_producer']
        new_price = request.form['post_price_new']
        old_price = request.form['post_price_old']
        category = request.form['post_category']
        link = request.form['post_link']
        update_deal_data(id, name, producer, new_price, old_price, link, category)
        return redirect(url_for("show_deal", id=id))


@app.route('/categories')
@login_required
def categories():
    """
    Shows a list of all categories.
    :return: Load template "categories.html"
    """
    return render_template("categories.html", title="Kategorien", categories=load_categories())


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def new_category():
    """
    Form to add a new category.
    :return: Redirect to referred page.
    """
    if request.method == 'POST':
        category = request.form['post_category']
        if check_category(category) is False:
            flash("Kategorie existiert bereits. Wähle eine andere Bezeichnung.", "warning")
            return redirect(request.referrer)
        else:
            save_category(category)
            flash("Die Kategorie wurde erfolgreich hinzugefügt!", "success")
            return redirect(request.referrer)


@app.route('/category/delete/<category>')
@login_required
def categories_delete_category(category):
    """
    Allows to delete a category.
    :param category: Name of the category.
    :return: Redirect to referred page.
    """
    delete_category(category)
    return redirect(request.referrer)


@app.route("/users")
@login_required
def users():
    """
    Show a list of all users.
    :return: Template "users.html"
    """
    return render_template("users.html", title="Users", users=load_users())


@app.route("/users/add", methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Allows to add a new user
    :return: redirect to users.html after adding the new user
    """
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        firstname = request.form['input_firstname']
        lastname = request.form['input_lastname']
        if check_username(username) == "taken":
            flash("Der Username existiert bereits!")
            redirect(url_for("users"))
        else:
            save_new_user(username, password, firstname, lastname)
            return redirect(url_for("users"))
    return render_template("users.html", users=load_users())


@app.route("/users/delete/<username>")
@login_required
def users_delete_user(username):
    """
    Allows to delete a user.
    :param username: Username of the user
    :return: Redirect vo referred page
    """
    delete_user(username)
    return redirect(request.referrer)


@app.errorhandler(404)
def not_found(e):
    """
    Load error page if url path is invalid
    Source: https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
    :return: login.html if not logged-in, else 404.html
    """
    if "USERNAME" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("404.html", title="Error 404")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
