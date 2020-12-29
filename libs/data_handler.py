"""
Contains all functions related to data management.
"""

import json
import math
import validators
from flask import session
from datetime import date
import os


# source: https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json'))
date = date.today().strftime('%d.%m.%Y')


def load_data():
    """
    Gets dictionary with all deals from (existing) JSON-file
    :return: Dict with all deals
    """
    try:
        with open(DATA_PATH, 'r') as db:
            deals = json.load(db)
    except:
        deals = {}

    return deals


def save_json(data):
    """
    Save dictionary to existing json file.
    :param data: Data source to save.
    """
    with open(DATA_PATH, 'w') as db:
        json.dump(data, db, indent=4)


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


def check_key(key):
    deals = load_data()
    keys = deals.keys()
    if key in keys:
        return True
    else:
        return False


def save_new_deal(id, name, producer, new_price, old_price, link, category):
    """
    Save data of a new deal into new or existing JSON-file
    :param link: URL to the product page (e.g. of the manufacturer)
    :param new_price: Discounted price
    :param old_price: Original price
    :param id: unique ID (given by id_handler)
    :param name: Name of the product
    :param category: Category of the deal
    """
    deals = load_data()
    discount = get_discount(new_price, old_price)
    deals[id] = {"user": session["USERNAME"], "name": name, "producer": producer, "new_price": new_price, "old_price": old_price,
                 "discount": discount, "link": link, "category": category, "date": str(date),
                 "accepted": [], "rejected": []}

    save_json(deals)


def update_deal_data(id, name, producer, new_price, old_price, link, category):
    """
    Update existing deal with new data
    :param link: URL to the product page (e.g. of the manufacturer)
    :param new_price: Discounted price
    :param old_price: Original price
    :param id: unique ID
    :param name: Name of the product
    :param category: Category of the deal
    """
    deals = load_data()
    discount = get_discount(new_price, old_price)
    deals[id]["name"] = name
    deals[id]["producer"] = producer
    deals[id]["new_price"] = new_price
    deals[id]["old_price"] = old_price
    deals[id]["discount"] = discount
    deals[id]["link"] = link
    deals[id]["category"] = category

    save_json(deals)


def delete_entry_byID(id):
    """
    Allows to delete a deal.
    :param id: Identifier of the deal
    """
    deals = load_data()
    del deals[id]
    save_json(deals)


def id_handler():
    """
    Create a unique ID for every entry deal.
    This function prevents duplicated IDs.
    :return: New (unique) ID
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
    Allows to vote for a deal.
    :param deal_id: Identifier of the deal.
    :param username: The user who has voted
    :param vote: What's the vote? Accepted / Rejected.
    """
    deals = load_data()
    deals[deal_id][vote].append(username)
    save_json(deals)


def get_voting(deal_id):
    """
    Get a list with votings of a specific deal.
    :param deal_id: Identifier of the deal.
    :return: Two lists with all users who have accepted/rejected + length of each list
    """
    deals = load_data()
    list_accepted = deals[deal_id]["accepted"]
    list_rejected = deals[deal_id]["rejected"]
    list_accepted_length = len(deals[deal_id]["accepted"])
    list_rejected_length = len(deals[deal_id]["rejected"])
    return list_accepted, list_rejected, list_accepted_length, list_rejected_length


def check_price(new_price, old_price):
    if float(new_price) >= float(old_price):
        return False
    else:
        pass


def get_discount(new_price, old_price):
    """
    Calculate the discount between the old and new price.
    :param new_price: Discounted price
    :param old_price: Original price
    :return: Calculated discount
    """
    calc_diff = (float(new_price) / float(old_price))
    discount = round((1 - calc_diff) * 100)
    return discount


def check_url_input(url_input):
    """
    Source: https://www.codespeedy.com/check-if-a-string-is-a-valid-url-or-not-in-python
    Check if entered URL is a valid URL
    :param url_input: User input with the URL
    :return: True if input is a valid URL, False if not.
    """
    validation = validators.url(url_input)
    if validation == True:
        return True
    else:
        return False
