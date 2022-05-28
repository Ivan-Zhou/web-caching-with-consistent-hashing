import pandas as pd
from PIL import Image
from io import BytesIO



def get_test_urls(n):
	df = pd.read_csv("test/test_data.csv")[:n]
	return df["url"].tolist()


def load_image_content(content):
	return Image.open(BytesIO(content))


def save_image(image, out_path="image.jpg"):
	image.save(out_path, 'JPEG')
