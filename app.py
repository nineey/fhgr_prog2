from flask import Flask
from flask import render_template
from flask import request
from libs.entries import Entry

entry = Entry()
print(entry.dict_entries)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/new', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        deal = request.form['deal_input']
        price = request.form['price_input']
        entry.new_entry(deal, price)
        print(entry.dict_entries)
        return "Vielen Dank für deine Eingabe!"
    return render_template("new_entry.html")


@app.route("/test")
def test():
    return "success"


if __name__ == "__main__":
    app.run(debug=True, port=5000)

