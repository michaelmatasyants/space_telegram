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


def check_create_path(path_to_save):
    Path(path_to_save).mkdir(parents=True, exist_ok=True)


def save_image(bytes_image, path_to_save, image_name="image.png"):
    with Image.open(BytesIO(bytes_image)) as new_image:
        new_image.save(Path(path_to_save, image_name))
    print(f'File {image_name} has been succesfully downloaded to',
          path_to_save)


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


def find_paths_to_images(path_to_search, count_of_images=1):
    paths_to_images = []
    for root, dirs, files in os.walk(path_to_search):
        for file in files:
            if file.endswith(('.png', '.jpeg', '.jpg')):
                if count_of_images == 1:
                    return Path(root, file)
                else:
                    paths_to_images.append(Path(root, file))
    return paths_to_images
