import json

data = {"key": "value"}

# create JSON file and add dict
def write_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


# load JSON
def read_json():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data


print(read_json())
