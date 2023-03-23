import requests
import argparse
from datetime import date, datetime
import api_tools
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os


def download_apod(image_link, to_save_path):
    image_response = requests.get(image_link)
    image_response.raise_for_status()
    api_tools.save_image(image_response.content, to_save_path,
                         ''.join(api_tools.get_filename_extension(image_link)))


def is_correct_date_format(*dates):
    for date in [*dates]:
        if date is not None:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return False
    return True


def main():
    load_dotenv(find_dotenv())
    nasa_api_key = os.environ["NASA_API_KEY"]
    image_parser = argparse.ArgumentParser(
        description='''Program downloads Astronomy Picture Of the Day (APOD).
                       If no date (or start_date, end_date) and path are given,
                       the program will download pictures of the curent day
                       and place picture(s) in the folder "images", located in
                       the project directory. If such a folder doesn't exist,
                       it'll be created automatically.'''
    )
    image_parser.add_argument("-p", "--path", default='images', type=Path,
                              help="enter path to save the image")
    image_parser.add_argument("-d", "--date",
                              help='''enter date (YYYY-MM-DD) to download
                              only 1 APOD''')
    image_parser.add_argument("-s", "--start_date",
                              help="""enter start_date for period to download
                                      a few APOD""")
    image_parser.add_argument("-e", "--end_date",
                              help="""enter end_date for period to download
                                      a few APOD""")
    args = image_parser.parse_args()
    if not is_correct_date_format(args.date, args.start_date, args.end_date):
        print("Please, make sure that the date format is correct.")
        return
    api_tools.check_create_path(args.path)
    url = "https://api.nasa.gov/planetary/apod"

    if args.start_date is None and args.end_date is None:
        if args.date is None:
            args.date = date.today()
        payload = {
            "api_key": f"{nasa_api_key}",
            "date": f"{args.date}"
        }
        try:
            apod_response = requests.get(url, params=payload)
            apod_response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            return print("Please, make sure that the NASA_API_KEY you've",
                         f"entered is correct.\n{http_err}")
        if apod_response.json()['media_type'] == 'image':
            try:
                image_link = apod_response.json()["hdurl"]
            # The next day's photo isn't immediately available
            # when that day occurs.
            except KeyError:
                return print(f"There is no picture for {args.date}.",
                             "Please try to enter any another date.")
            download_apod(image_link, args.path)
    else:
        payload = {
            "api_key": f"{nasa_api_key}",
            "start_date": f"{args.start_date}",
            "end_date": f"{args.end_date}"
        }
        try:
            apod_response = requests.get(url, params=payload)
            apod_response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            return print("Please, make sure that the NASA_API_KEY you've",
                         f"entered is correct.\n{http_err}")
        apod_links = []
        for response in apod_response.json():
            if response['media_type'] == 'image':
                try:
                    apod_links.append(response["hdurl"])
                except KeyError:
                    print(f"There is no picture for {args.date}.")
        for image_link in apod_links:
            download_apod(image_link, args.path)


if __name__ == "__main__":
    main()
