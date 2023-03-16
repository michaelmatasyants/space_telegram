import requests
import argparse
import os
from datetime import date, datetime
import spacex_nasa_api
from pathlib import Path


def download_apod(image_link, path_to_save):
    image_response = requests.get(image_link)
    image_response.raise_for_status()
    spacex_nasa_api.save_image(
        image_response.content, path_to_save,
        ''.join(spacex_nasa_api.get_filename_extension(image_link))
        )


def is_date_format_correct(*dates):
    for date in [*dates]:
        if date is not None:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return False
    return True


def main():
    nasa_api_key = spacex_nasa_api.get_api_key()['nasa_api_key']
    image_parser = argparse.ArgumentParser(
        description='''Program downloads Astronomy Picture Of the Day (APOD).
                       If no date (or start_date, end_date) and path are given,
                       the program will download pictures for the curent day
                       and place them on Windows desktop and in /home/user on
                       Linux'''
    )
    image_parser.add_argument("-p", "--path", default=os.path.expanduser("~"),
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
    if not is_date_format_correct(args.date, args.start_date, args.end_date):
        return print("Please, make sure that the date format is correct.")
    spacex_nasa_api.check_create_path(Path(args.path))
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
            image_link = apod_response.json()["hdurl"]
            download_apod(image_link, Path(args.path))
        except requests.exceptions.HTTPError as http_err:
            print("Please, make sure that the NASA_API_KEY you've entered is",
                  f"correct.\n{http_err}")
    else:
        payload = {
            "api_key": f"{nasa_api_key}",
            "start_date": f"{args.start_date}",
            "end_date": f"{args.end_date}"
        }
        try:
            apod_response = requests.get(url, params=payload)
            apod_response.raise_for_status()
            links_apod = [i["hdurl"] for i in apod_response.json()]
            for image_link in links_apod:
                download_apod(image_link, Path(args.path))
        except requests.exceptions.HTTPError as http_err:
            print("Please, make sure that the NASA_API_KEY you've entered is",
                  f"correct.\n{http_err}")


if __name__ == "__main__":
    main()
