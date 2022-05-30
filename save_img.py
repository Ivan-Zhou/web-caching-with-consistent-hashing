import requests
import pandas as pd
from PIL import Image
from io import BytesIO

from test.utils import get_test_urls, load_image_content, save_image


def save_all_imgs():
    test_urls = get_test_urls(n=3)
    for i, url in enumerate(test_urls):
        image = load_image_content(requests.get(url).content)
        save_image(image, out_path=f"./images/{i}.jpg")



if __name__ == '__main__':
    save_all_imgs()

    