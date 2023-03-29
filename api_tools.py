import os
from urllib.parse import urlparse, unquote
from pathlib import Path
from io import BytesIO
from PIL import Image
import telegram
import requests


def get_filename_extension(image_url: str) -> tuple:
    root, extension = os.path.splitext(urlparse(unquote(image_url)).path)
    filename = root.split('/')[-1]
    return filename, extension


def check_create_path(save_path: Path):
    save_path.mkdir(parents=True, exist_ok=True)


def save_image(bytes_image, save_path, image_name="image.png"):
    with Image.open(BytesIO(bytes_image)) as new_image:
        new_image.save(Path(save_path, image_name))


def publish_image_as_file(photo_path: Path, tg_bot_token: str,
                          tg_chat_id: str):
    bot = telegram.Bot(tg_bot_token)
    with open(photo_path, 'rb') as new_image:
        bot.send_document(tg_chat_id, document=new_image)


def has_photo_extension(some_path: Path) -> bool:
    return some_path.suffix in ('.png', '.jpeg', '.jpg')


def find_image_paths(searched_path: Path, image_quantity=1) -> Path | list:
    image_paths = []
    for root, dirs, files in os.walk(searched_path):
        for file in files:
            file_path = Path(root, file)
            if has_photo_extension(file_path):
                if image_quantity == 1:
                    return file_path
                image_paths.append(file_path)
    return image_paths


def get_response(url: str, payload: dict) -> requests.models.Response:
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response


def download_image(image_link: str, to_save_path: Path,
                   added_to_the_top_of_image_name=None, payload=None) -> str:
    image_response = requests.get(image_link, payload)
    image_response.raise_for_status()
    image_name = "".join(get_filename_extension(image_link))
    if added_to_the_top_of_image_name:
        image_name = f'{added_to_the_top_of_image_name}_{image_name}'
    save_image(image_response.content, to_save_path, image_name)
    return image_name


def download_all_images(image_links: list, to_save_path: Path,
                        added_to_the_top_of_image_name=None,
                        payload=None) -> list:
    image_names = [download_image(image_link, to_save_path,
                                  added_to_the_top_of_image_name, payload)
                   for image_link in image_links]
    return image_names
