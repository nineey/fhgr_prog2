import json


# create JSON file and add dict
def save_data(id, deal, price):
    try:
        with open('data/data.json', 'r') as db:
            deals = json.load(db)
    except:
        deals = {}

    deals[id] = {"name": deal, "price": price}

    with open('data/data.json', 'w') as db:
        json.dump(deals, db, indent=4)


# load JSON
def load_data():
    with open('data/data.json', 'r') as db:
        deals = json.load(db)
    return deals


# handle unique ID
def id_handler():
    try:
        deals = load_data()
        key_list = deals.keys()
        max_key = max(key_list)
        new_id = int(max_key) + 1
    except:
        new_id = 1

    return new_id


# get users
def load_users():
    with open('data/users.json', 'r') as db:
        users = json.load(db)
    return users
