import json
import math

from flask import session
from datetime import date

date = date.today().strftime('%d.%m.%Y')


def load_data():
    """
    gets a dictionary with all deals from (existing) JSON-file
    :return: dict with all deals
    """
    try:
        with open("data/data.json", 'r') as db:
            deals = json.load(db)
    except:
        deals = {}

    return deals


def load_data_range(start, count):
    deals = load_data()
    keys = deals.keys()
    keys = [int(i) for i in keys]
    keys = list(reversed(keys))
    max_pages = math.ceil((len(keys)) / 10)

    sliced_keys = keys[start:start + count]

    deals_to_return = {}
    for key in sliced_keys:
        deals_to_return[str(key)] = deals[str(key)]

    return deals_to_return, max_pages


def save_data(id, deal, price, category):
    """
    Saves data of a new deal into new or existing JSON-file
    :param id: unique ID (given by id_handler)
    :param deal: name of the deal
    :param price: price of the deal
    :param category: category of the deal
    """
    deals = load_data()
    deals[id] = {"user": session["USERNAME"], "name": deal, "price": price, "category": category, "date": str(date),
                 "accepted": [], "rejected": []}

    with open('data/data.json', 'w') as db:
        json.dump(deals, db, indent=4)


def id_handler():
    """
    every deal must have a unique ID for identification reasons
    this function prevents duplicated IDs
    :return: new (unique) ID
    """
    try:
        deals = load_data()
        key_list = deals.keys()
        # list comprehension to form dict_keys into list with integers
        int_key_list = [int(i) for i in key_list]
        new_id = max(int_key_list) + 1
    except:
        new_id = 1

    return new_id


def add_voting(deal_id, username, vote):
    deals = load_data()
    deals[deal_id][vote].append(username)
    with open('data/data.json', 'w') as db:
        json.dump(deals, db, indent=4)


def get_voting(deal_id):
    deals = load_data()
    list_accepted = deals[deal_id]["accepted"]
    list_rejected = deals[deal_id]["rejected"]
    list_accepted_length = len(deals[deal_id]["accepted"])
    list_rejected_length = len(deals[deal_id]["rejected"])
    return list_accepted, list_rejected, list_accepted_length, list_rejected_length


def check_price(user_input):
    try:
        user_input = int(user_input)
        return True
    except ValueError:
        try:
            user_input = float(user_input)
            return True
        except ValueError:
            return False





