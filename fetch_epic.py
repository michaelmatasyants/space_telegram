import os
import argparse
from datetime import datetime
from pathlib import Path
import requests
from dotenv import find_dotenv, load_dotenv
from api_tools import check_create_path, download_all_images, get_response


def get_link_to_photo(about_image_response: dict, extension: str) -> (
        str | None):
    image_date = datetime.fromisoformat(about_image_response.get('date')
        ).strftime("%Y/%m/%d")
    image_name = f"{about_image_response['image']}.{extension}"
    image_link = "https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}".format(
                    image_date, extension, image_name)
    return image_link


def get_links_to_all_photos(about_images_response: requests.models.Response,
                            extension: str) -> list:
    image_links = [get_link_to_photo(about_image_response, extension)
                   for about_image_response in about_images_response.json()]
    return image_links


def main():
    load_dotenv(find_dotenv())

    image_parser = argparse.ArgumentParser(
        description='''Program downloads natural color images of The Earth
                       taken by the NASA Earth Polychromatic Imaging Camera
                       (EPIC). If you don't specify an image extension and
                       save path, the program will download image(s) with "PNG"
                       extension and place in the "images" folder located in
                       the project directory. If such a folder doesn't exist,
                       it'll be created automatically.'''
    )
    image_parser.add_argument("-p", "--path", default='images', type=Path,
                              help="enter path to save the image")
    image_parser.add_argument("-x", "--extension", default='png',
                              help="enter extension for the image png or jpg")
    args = image_parser.parse_args()
    check_create_path(args.path)
    payload = {"api_key": f"{os.environ['NASA_API_KEY']}"}
    try:
        about_images_response = get_response(
            "https://api.nasa.gov/EPIC/api/natural", payload)
    except requests.exceptions.HTTPError as http_err:
        print(f"{http_err}\n", "Please, make sure that the NASA_API_KEY",
              "you've entered in .env file is correct.")
        return
    epic_links = get_links_to_all_photos(about_images_response, args.extension)
    downloaded_image_names = download_all_images(epic_links, args.path,
                                                 payload=payload)
    print(*downloaded_image_names, sep=', ', end=' ')
    print(f'successfully downloaded to {args.path}.')


if __name__ == "__main__":
    main()
