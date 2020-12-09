"""
Contains all functions related to categories.
"""

import json


def save_category(category):
    """
    Save new category to existing or new JSON-file
    :param category: Name of the new category
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
    Get a list of categories from JSON-file
    :return: List of all categories
    """
    try:
        with open('data/categories.json', 'r') as file:
            categories = json.load(file)
    except:
        categories = []

    return categories


def delete_category(category):
    """
    Allows to delete a category
    :param category: Name of the category
    """
    categories = load_categories()
    categories.remove(category)
    with open('data/categories.json', 'w') as db:
        json.dump(categories, db)


def check_category(category):
    """
    Check if category already exists.
    :param category: Name of the category.
    :return: If category already exist, return False
    """
    categories = load_categories()
    if category.capitalize() in categories:
        return False
    else:
        pass
