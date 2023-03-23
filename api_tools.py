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


def check_create_path(save_path):
    save_path.mkdir(parents=True, exist_ok=True)


def save_image(bytes_image, save_path, image_name="image.png"):
    with Image.open(BytesIO(bytes_image)) as new_image:
        new_image.save(Path(save_path, image_name))
    print(f'File {image_name} has been succesfully downloaded to',
          save_path)


def publish_message(text):
    load_dotenv(find_dotenv())
    bot = telegram.Bot(token=os.environ['TG_BOT_TOKEN'])
    bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text=text)


def publish_image_as_file(photo_path):
    load_dotenv(find_dotenv())
    bot = telegram.Bot(token=os.environ['TG_BOT_TOKEN'])
    with open(photo_path, 'rb') as new_image:
        bot.send_document(chat_id=os.environ['TG_CHAT_ID'],
                          document=new_image)


def find_image_paths(searched_path, image_quantity=1):
    image_paths = []
    for root, dirs, files in os.walk(searched_path):
        for file in files:
            if file.endswith(('.png', '.jpeg', '.jpg')):
                if image_quantity == 1:
                    return Path(root, file)
                else:
                    image_paths.append(Path(root, file))
    return image_paths
