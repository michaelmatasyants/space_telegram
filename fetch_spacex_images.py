import requests
from pathlib import Path
import argparse
import os
from spacex_nasa_api import save_image, check_create_path
from spacex_nasa_api import get_filename_extension


def get_links_to_photos(launch_id):
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(f'{url}/{launch_id}')
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def main():
    image_parser = argparse.ArgumentParser(
        description='''Program downloads pictures of SpaceX launches.
                    If no 'ID' and 'Path' are given, the program will
                    download pictures from the last launch and place them
                    on Windows desktop and in /home/user on Linux'''
    )
    image_parser.add_argument('-i', '--id', default='latest', type=str,
                              help='enter the launch ID to download images.')
    image_parser.add_argument('-p', '--path', default=os.path.expanduser('~'),
                              help='enter path to save the image')
    args = image_parser.parse_args()
    check_create_path(Path(args.path))
    try:
        links_launch_images = get_links_to_photos(args.id)
        if links_launch_images:
            image_quantity = len(links_launch_images)
            for url_id, url in enumerate(links_launch_images):
                try:
                    response_image = requests.get(url)
                    response_image.raise_for_status()
                    save_image(response_image.content, Path(args.path),
                               '{}_{}'.format(
                        url_id, "".join(get_filename_extension(url)))
                        )
                except requests.exceptions.HTTPError:
                    image_quantity -= 1
                    if not image_quantity:
                        print(f"All links to images from {args.id} launch",
                              "are invalid. Try to download images of another",
                              "launch.")
        else:
            print(f"No pictures from {args.id} launch.")
    except requests.exceptions.HTTPError:
        print('''You've entered incorrect "id".''')


if __name__ == "__main__":
    main()
