import requests
import spacex_nasa_api
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os


def downlaod_epic_images(url, payload, extension, path_to_save):
    about_all_images = requests.get(f"{url}/api/natural", params=payload)
    about_all_images.raise_for_status()
    for about_image in about_all_images.json():
        date_image = datetime.fromisoformat(
            about_image['date']).strftime("%Y/%m/%d")
        name_image = f"{about_image['image']}.{extension}"
        image_url = "{}/archive/natural/{}/{}/{}".format(
            url, date_image, extension, name_image)
        image_response = requests.get(image_url, params=payload)
        image_response.raise_for_status()
        spacex_nasa_api.save_image(image_response.content,
                                   Path(path_to_save),
                                   name_image)


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
    image_parser.add_argument("-p", "--path", default=Path('images'),
                              help="enter path to save the image")
    image_parser.add_argument("-x", "--extension", default='png',
                              help="enter extension for the image png or jpg")
    args = image_parser.parse_args()
    spacex_nasa_api.check_create_path(Path(args.path))
    url = "https://api.nasa.gov/EPIC"
    payload = {"api_key": f"{os.environ['NASA_API_KEY']}"}
    try:
        downlaod_epic_images(url, payload, args.extension, args.path)
    except requests.exceptions.HTTPError as http_err:
        return print("Please, make sure that the NASA_API_KEY you've entered",
                     f"is correct.\n{http_err}")


if __name__ == "__main__":
    main()
