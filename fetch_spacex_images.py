import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import argparse
import os


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
    Path(args.path).mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(
            f"https://api.spacexdata.com/v5/launches/{args.id}"
            )
        response.raise_for_status()
        links_launch_images = response.json()["links"]["flickr"]["original"]
        if links_launch_images:
            for id, url in enumerate(links_launch_images):
                response_image = requests.get(url)
                with Image.open(BytesIO(response_image.content)) as new_image:
                    new_image.save(Path(args.path,
                                        f'{id}.spacex_{args.id}.jpg'))
        else:
            print(f"No pictures from {args.id} launch.")
    except requests.exceptions.HTTPError:
        print('''You've entered incorrect "id".''')


if __name__ == "__main__":
    main()
