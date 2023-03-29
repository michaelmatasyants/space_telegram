from pathlib import Path
import argparse
import os
from dotenv import load_dotenv, find_dotenv
import fetch_apod
from api_tools import (find_image_paths, publish_image_as_file,
                       has_photo_extension)


def is_photo_path(photo_path: Path) -> bool:
    return os.path.isfile(photo_path) and has_photo_extension(photo_path)


def directory_contains_photo(direcory: Path) -> bool:
    return find_image_paths(direcory, image_quantity=1)


def main():
    load_dotenv(find_dotenv())
    bot_token, chat_id = os.environ['TG_BOT_TOKEN'], os.environ['TG_CHAT_ID']
    parser = argparse.ArgumentParser(
        description="""The program publishes one picture from given path or
                       directory. But if the path isn't given program will
                       download APOD for the current day and publish it. After
                       publication picture would be deleted."""
    )
    parser.add_argument('-p', '--photo_path', default='images', type=Path,
                        help='''path to the directory with the photo to be
                        published''')
    args = parser.parse_args()
    if is_photo_path(args.photo_path):
        publish_image_as_file(args.photo_path, bot_token, chat_id)
        return
    if directory_contains_photo(args.photo_path):
        publish_image_as_file(find_image_paths(args.photo_path),
                              bot_token, chat_id)
        return
    fetch_apod.main()
    published_photo = find_image_paths(args.photo_path)
    publish_image_as_file(published_photo, bot_token, chat_id)
    os.remove(published_photo)
    print("The file was deleted from your computer after publication")


if __name__ == "__main__":
    main()
