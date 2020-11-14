"""
Contains all functions related to categories.
"""

import json


def save_category(category):
    """
    save new category to existing or new JSON-file
    :param category: user input of new category
    """
    try:
        with open('data/categories.json', 'r') as file:
            categories = json.load(file)
    except:
        categories = []

    categories.append(category)

    with open('data/categories.json', 'w') as file:
        json.dump(categories, file)


def load_categories():
    """
    function to get list a categories from JSON-file
    :return: list of all categories
    """
    try:
        with open('data/categories.json', 'r') as file:
            categories = json.load(file)
    except:
        categories = []

    return categories
