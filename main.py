import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
from urllib.parse import urlparse, unquote
import datetime


def check_or_create_path(entered_path):
    Path(entered_path).mkdir(parents=True, exist_ok=True)


def get_filename_and_extension(image_url):
    root, extension = os.path.splitext(urlparse(unquote(image_url)).path)
    filename = root.split("/")[-1]
    return filename, extension


def fetch_spacex_launch(path_to_save, id='latest'):
    check_or_create_path(path_to_save)
    try:
        response = requests.get(f"https://api.spacexdata.com/v5/launches/{id}")
        response.raise_for_status()
        links_flight_images = response.json()["links"]["flickr"]["original"]

        if links_flight_images:
            for id, url in enumerate(links_flight_images):
                response_image = requests.get(url)
                with Image.open(BytesIO(response_image.content)) as new_image:
                    new_image.save(f"{path_to_save}/spacex_{id}.jpg")
        else:
            print(f"No pictures from {id} flight.")
    except requests.exceptions.HTTPError:
        print('''You've entered incorrect "id".''')


def download_apod(path_to_save, date="", start_date="", end_date=""):
    check_or_create_path(path_to_save)
    print("\nEnter date (YYYY-MM-DD) to download only 1 Astronomy",
          "Picture of the Day(APOD)\nor skip(press ENTER) to download",
          "more than 1 image:")
    date = input()
    if not date:
        print("\nEnter 'start date' and 'end date' to download a few APOD.")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
    print("Downloading Astronomy Picture of the Day...")

    load_dotenv(find_dotenv())
    nasa_api_key = os.environ["NASA_API_KEY"]
    url = "https://api.nasa.gov/planetary/apod"
    payload = {
        "api_key": f"{nasa_api_key}",
        "date": f"{date}",
        "start_date": f"{start_date}",
        "end_date": f"{end_date}"
    }

    apod_response = requests.get(url, params=payload)
    if start_date and end_date:
        links_apod = [i["hdurl"] for i in apod_response.json()]
        for link in links_apod:
            filename, extension = get_filename_and_extension(link)
            image_response = requests.get(link).content
            with Image.open(BytesIO(image_response)) as new_image:
                new_image.save(f"{path_to_save}/{filename}{extension}")
            print(requests.get(link).url)
    else:  # Download only 1 APOD by date
        image_link = apod_response.json()["hdurl"]
        filename, extension = get_filename_and_extension(image_link)
        image_response = requests.get(image_link).content
        with Image.open(BytesIO(image_response)) as new_image:
            new_image.save(f"{path_to_save}/{filename}{extension}")
    print("All images have been downloaded!\n")


def download_epic(path_to_save, extension="png"):
    print("Downloading daily natural color imagery of Earth(EPIC)...")
    check_or_create_path(path_to_save)
    load_dotenv(find_dotenv())
    nasa_api_key = os.environ["NASA_API_KEY"]
    data_gathering_url = "https://api.nasa.gov/EPIC/api/natural"
    payload = {
        "api_key": f"{nasa_api_key}"
    }
    about_image_response = requests.get(
        data_gathering_url, params=payload
        ).json()
    for id in range(len(about_image_response)):
        date_image = datetime.datetime.fromisoformat(
            about_image_response[id]["date"]
            ).strftime("%Y/%m/%d")
        name_image = f"{about_image_response[id]['image']}.{extension}"

        image_url = "https://api.nasa.gov/EPIC/archive/natural/{date_image}/{extension}/{name_image}"
        image_response = requests.get(image_url, params=payload)
        with Image.open(BytesIO(image_response.content)) as new_image:
            new_image.save(f"{path_to_save}/{name_image}")
    print("All images have been downloaded!")


def main():
    new_path = input("Enter a path to save images: ")
    fetch_spacex_launch(f"{new_path}/images", "5eb87d42ffd86e000604b384")
    download_apod(f"{new_path}/nasa_apod")
    download_epic(f"{new_path}/nasa_epic")


if __name__ == "__main__":
    main()
