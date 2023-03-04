import os
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse, unquote
from pathlib import Path
from io import BytesIO
from PIL import Image

# Create a commit "Make the functions suitable for telegram bot as well"  In the end привести к единому виду все файлы, причесав код

def get_filename_extension(image_url):
    root, extension = os.path.splitext(urlparse(unquote(image_url)).path)
    filename = root.split('/')[-1]
    return filename, extension


def get_api_key():
    load_dotenv(find_dotenv())
    api_keys = {
        'nasa_api_key': os.environ['NASA_API_KEY'],
        'tg_api_key': os.environ['TG_TOKEN'],
        'chat_id': os.environ['CHAT_ID']
        }
    return api_keys


def check_create_path(path_to_save):
    Path(path_to_save).mkdir(parents=True, exist_ok=True)


def save_image(bytes_image, path_to_save, image_name="image.png"):
    Image.open(BytesIO(bytes_image)).save(f"{path_to_save}/{image_name}")
