import pandas as pd
from PIL import Image
from io import BytesIO
import json
DATA_FILE = "../data.json"


def get_test_urls(n):
	df = pd.read_csv("test/test_data.csv")[:n]
	return df["url"].tolist()


def load_image_content(content):
	return Image.open(BytesIO(content))


def save_image(image, out_path="image.jpg"):
	image.save(out_path, 'JPEG')

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def get_webserver_address():
    data = load_data()
    return data["webserver"]

def get_section_num():
    data = load_data()
    return data["section_num"]
