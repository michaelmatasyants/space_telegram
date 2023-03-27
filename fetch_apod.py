import requests
import argparse
from datetime import date, datetime
import api_tools
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os


def is_correct_date_format(*dates: datetime.date) -> bool:
    for date in [*dates]:
        if date is not None:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return False
    return True


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


def get_apod_response(url: str, payload: dict) -> (
        requests.models.Response | None):
    try:
        apod_response = requests.get(url, params=payload)
        apod_response.raise_for_status()
        return apod_response
    except requests.exceptions.HTTPError as http_err:
        print(http_err)


def get_link_to_photo(apod_response: dict | requests.models.Response) -> (
        str | None):
    # The next day's photo isn't immediately available when that day occurs.
    if apod_response['media_type'] == 'image':
        try:
            image_link = apod_response["hdurl"]
            return image_link
        except KeyError:
            return


def get_links_to_all_photos(apod_response: requests.models.Response) -> list:
    apod_links = [get_link_to_photo(response)
                  for response in apod_response.json()
                  if get_link_to_photo(response) is not None]
    return apod_links


def download_apod(image_link: str, to_save_path: Path):
    image_response = requests.get(image_link)
    image_response.raise_for_status()
    image_name = ''.join(api_tools.get_filename_extension(image_link))
    api_tools.save_image(image_response.content, to_save_path, image_name)
    print(f'File {image_name} has been successfully downloaded to',
          to_save_path)


def download_all_apods(image_links, to_save_path):
    for image_link in image_links:
        download_apod(image_link, to_save_path)


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
    api_tools.check_create_path(args.path)
    url = "https://api.nasa.gov/planetary/apod"
    if not is_correct_date_format(args.date, args.start_date, args.end_date):
        print("Please, make sure that the date format is correct.")
        return
    payload = get_payload(args.date, args.start_date,
                          args.end_date, nasa_api_key)
    if get_apod_response(url, payload) is None:
        print("Please, make sure that the NASA_API_KEY you've entered in .env",
              "file is correct")
        return
    apod_response = get_apod_response(url, payload)

    if args.start_date is None and args.end_date is None:
        if get_link_to_photo(apod_response.json()) is None:
            print(f"There is no picture for {args.date}.",
                  "Please try to enter any another date.")
            return
        apod_link = get_link_to_photo(apod_response.json())
        download_apod(apod_link, args.path)
        return

    if not get_links_to_all_photos(apod_response):
        print(f"No photos from {args.start_date} to {args.end_date}.")
        return
    apod_links = get_links_to_all_photos(apod_response)
    download_all_apods(apod_links, args.path)


if __name__ == "__main__":
    main()
