import json
from flask import session
from datetime import date

date = date.today().strftime('%d.%m.%Y')


# create JSON file and add dict
def save_data(id, deal, price, category):
    try:
        with open('data/data.json', 'r') as db:
            deals = json.load(db)
    except:
        deals = {}

    deals[id] = {"user": session["USERNAME"], "name": deal, "price": price, "category": category, "date": str(date)}

    with open('data/data.json', 'w') as db:
        json.dump(deals, db, indent=4)


# load JSON
def load_data():
    with open("data/data.json", 'r') as db:
        deals = json.load(db)
    return deals


# handle unique ID
def id_handler():
    try:
        deals = load_data()
        key_list = deals.keys()
        int_key_list = [int(i) for i in key_list]
        new_id = max(int_key_list) + 1
    except:
        new_id = 1

    return new_id


