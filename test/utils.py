import pandas as pd
from PIL import Image
from io import BytesIO
import json
ADDRESS_DATA_FILE = "../data.json"


    

def get_test_urls(n):
	df = pd.read_csv("test/test_data.csv")[:n]
	return df["url"].tolist()


def load_image_content(content):
	return Image.open(BytesIO(content))


def save_image(image, out_path="image.jpg"):
	image.save(out_path, 'JPEG')

def get_address_data():
    with open(ADDRESS_DATA_FILE, "r") as f:
        return json.load(f)

def get_webserver_address():
    address_data = get_address_data()
    return address_data["webserver"]

def get_section_num():
    address_data = get_address_data()
    return address_data["section_num"]
