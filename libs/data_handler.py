import json
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


def save_data(id, deal, price, category):
    """
    Saves data of a new deal into new or existing JSON-file
    :param id: unique ID (given by id_handler)
    :param deal: name of the deal
    :param price: price of the deal
    :param category: category of the deal
    """
    deals = load_data()
    deals[id] = {"user": session["USERNAME"], "name": deal, "price": price, "category": category, "date": str(date), "voting": {}}

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
    """
    function to add a user voting to a specific deal and save to JSON
    :param deal_id: unique id to identify the deal
    :param username: who has voted?
    :param vote: accepted or rejected?
    """
    deals = load_data()
    deals[deal_id]["voting"][username] = vote
    with open('data/data.json', 'w') as db:
        json.dump(deals, db, indent=4)