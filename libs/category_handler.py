import json


# category handler


def save_category(category):
    try:
        with open('../data/categories.json', 'r') as file:
            categories = json.load(file)
    except:
        categories = []

    categories.append(category)

    with open('../data/categories.json', 'w') as file:
        json.dump(categories, file)


# load JSON
def load_categories():
    with open('data/categories.json', 'r') as file:
        categories = json.load(file)
    return categories
