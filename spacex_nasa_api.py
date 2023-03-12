import os
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse, unquote
from pathlib import Path
from io import BytesIO
from PIL import Image
import telegram


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
    with Image.open(BytesIO(bytes_image)) as new_image:
        new_image.save(Path(path_to_save, image_name))


def publish_message(text):
    bot = telegram.Bot(token=get_api_key()['tg_api_key'])
    bot.send_message(chat_id=get_api_key()['chat_id'], text=text)


def publish_image_as_file(photo_path):
    bot = telegram.Bot(token=get_api_key()['tg_api_key'])
    with open(photo_path, 'rb') as new_image:
        bot.send_document(chat_id=get_api_key()['chat_id'], document=new_image)
