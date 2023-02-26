import requests
import argparse
import os
from datetime import date
from PIL import Image
from io import BytesIO
from spacex_nasa_api import get_api_key, check_create_path
from spacex_nasa_api import get_filename_extension


def main():
    nasa_api_key = get_api_key()
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
    check_create_path(args.path)
    url = "https://api.nasa.gov/planetary/apod"

    if args.start_date is None and args.end_date is None:
        if args.date is None:
            args.date = date.today()
        payload = {
            "api_key": f"{nasa_api_key}",
            "date": f"{args.date}"
        }
    else:
        payload = {
            "api_key": f"{nasa_api_key}",
            "start_date": f"{args.start_date}",
            "end_date": f"{args.end_date}"
        }
    apod_response = requests.get(url, params=payload)
    if args.start_date and args.end_date:
        links_apod = [i["hdurl"] for i in apod_response.json()]
        for image_link in links_apod:
            filename, extension = get_filename_extension(image_link)
            image_response = requests.get(image_link)
            Image.open(BytesIO(image_response.content)).save(
                f"{args.path}/{filename}{extension}"
                )
            print(f'''File {filename}{extension} has been succesfully
                      downloaded''')
    else:
        image_link = apod_response.json()["hdurl"]
        filename, extension = get_filename_extension(image_link)
        image_response = requests.get(image_link)
        Image.open(BytesIO(image_response.content)).save(
            f"{args.path}/{filename}{extension}"
            )
        print(f'File "{filename}{extension}" has been successfully downloaded')


if __name__ == "__main__":
    main()
