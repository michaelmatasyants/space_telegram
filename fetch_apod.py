import os
from datetime import date, datetime
import argparse
from pathlib import Path
import requests
from dotenv import find_dotenv, load_dotenv
from api_tools import (check_create_path, download_image,
                       download_all_images, get_response)


def is_correct_date_format(*dates: datetime.date):
    for some_date in [*dates]:
        if some_date is not None:
            datetime.strptime(some_date, "%Y-%m-%d")


def get_payload(date: datetime.date, start_date: datetime.date,
                end_date: datetime.date, api_key: str) -> dict:
    if start_date is None and end_date is None:
        payload = {
            "api_key": f"{api_key}",
            "date": f"{date}"
        }
        return payload
    payload = {
        "api_key": f"{api_key}",
        "start_date": f"{start_date}",
        "end_date": f"{end_date}"
    }
    return payload


def get_link_to_photo(apod_response: dict | requests.models.Response) -> (
        str | None):
    if apod_response['media_type'] == 'image':
        return apod_response.get('hdurl')


def get_links_to_all_photos(apod_response: requests.models.Response) -> list:
    apod_links = [get_link_to_photo(response)
                  for response in apod_response.json()
                  if get_link_to_photo(response) is not None]
    return apod_links


def main():
    load_dotenv(find_dotenv())
    nasa_api_key = os.environ["NASA_API_KEY"]
    image_parser = argparse.ArgumentParser(
        description='''Program downloads Astronomy Picture Of the Day (APOD).
                       If no date (or start_date, end_date) and path are given,
                       the program will download pictures of the current day
                       and place picture(s) in the folder "images", located in
                       the project directory. If such a folder doesn't exist,
                       it'll be created automatically.'''
    )
    image_parser.add_argument("-p", "--path", default='images', type=Path,
                              help="enter path to save the image")
    image_parser.add_argument("-d", "--date",
                              default=date.today().strftime("%Y-%m-%d"),
                              help='''enter date (YYYY-MM-DD) to download only
                              1 APOD''')
    image_parser.add_argument("-s", "--start_date",
                              help="""enter start_date for period to download
                                      a few APOD""")
    image_parser.add_argument("-e", "--end_date",
                              help="""enter end_date for period to download
                                      a few APOD""")
    args = image_parser.parse_args()
    check_create_path(args.path)
    try:
        is_correct_date_format(args.date, args.start_date, args.end_date)
    except ValueError:
        print("Please, make sure that the date format is correct.")
        return
    payload = get_payload(args.date, args.start_date,
                          args.end_date, nasa_api_key)
    try:
        apod_response = get_response("https://api.nasa.gov/planetary/apod",
                                     payload)
    except requests.exceptions.HTTPError as http_err:
        print(f"{http_err}\n", "Please, make sure that the NASA_API_KEY",
              "you've entered in .env file is correct.")
        return

    if args.start_date is None and args.end_date is None:
        apod_link = get_link_to_photo(apod_response.json())
        if apod_link is None:
            print(f"There is no picture for {args.date}.",
                  "Please try to enter any another date.")
            return
        downloaded_image_name = download_image(apod_link, args.path)
        print(downloaded_image_name,
              f'successfully downloaded to {args.path}.')
        return

    apod_links = get_links_to_all_photos(apod_response)
    if not apod_links:
        print(f"No photos from {args.start_date} to {args.end_date}.")
        return
    downloaded_image_names = download_all_images(apod_links, args.path)
    print(*downloaded_image_names, sep=', ', end=' ')
    print(f'successfully downloaded to {args.path}.')


if __name__ == "__main__":
    main()
