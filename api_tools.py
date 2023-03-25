import os
from urllib.parse import urlparse, unquote
from pathlib import Path
from io import BytesIO
from PIL import Image
import telegram


def get_filename_extension(image_url) -> set:
    root, extension = os.path.splitext(urlparse(unquote(image_url)).path)
    filename = root.split('/')[-1]
    return filename, extension


def check_create_path(save_path: Path):
    save_path.mkdir(parents=True, exist_ok=True)


def save_image(bytes_image, save_path, image_name="image.png"):
    with Image.open(BytesIO(bytes_image)) as new_image:
        new_image.save(Path(save_path, image_name))


def publish_message(text: str, tg_bot_token: str, tg_chat_id: str):
    bot = telegram.Bot(tg_bot_token)
    bot.send_message(tg_chat_id, text=text)


def publish_image_as_file(photo_path: Path, tg_bot_token: str, tg_chat_id: str):
    bot = telegram.Bot(tg_bot_token)
    with open(photo_path, 'rb') as new_image:
        bot.send_document(tg_chat_id, document=new_image)


def find_image_paths(searched_path: Path, image_quantity=1) -> Path | list:
    image_paths = []
    for root, dirs, files in os.walk(searched_path):
        for file in files:
            if file.endswith(('.png', '.jpeg', '.jpg')):
                if image_quantity == 1:
                    return Path(root, file)
                image_paths.append(Path(root, file))
    return image_paths
