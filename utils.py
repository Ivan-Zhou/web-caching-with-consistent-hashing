import json

ADDRESS_DATA_FILE = "data.json"

def get_address_data():
    with open(ADDRESS_DATA_FILE, "r") as f:
        return json.load(f)


def get_master_address():
    address_data = get_address_data()
    return address_data["master"]
