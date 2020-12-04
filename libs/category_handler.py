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

    categories.append(category.capitalize())

    with open('data/categories.json', 'w') as file:
        json.dump(categories, file)


def load_categories():
    """
    function to get list of categories from JSON-file
    :return: list of all categories
    """
    try:
        with open('data/categories.json', 'r') as file:
            categories = json.load(file)
    except:
        categories = []

    return categories


def delete_category(category):
    """
    Function to delete a single category
    :param category: identifies the category to delete
    """
    categories = load_categories()
    categories.remove(category)
    with open('data/categories.json', 'w') as db:
        json.dump(categories, db)


def check_category(category):
    """
    check if category already exists
    :param category: user input of new category
    :return: if category already exist, return False
    """
    categories = load_categories()
    if category.capitalize() in categories:
        return False
    else:
        pass
