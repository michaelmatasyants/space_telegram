import requests
from pathlib import Path
import argparse
from api_tools import save_image, check_create_path, get_filename_extension


def get_links_to_photos(launch_id):
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(f'{url}/{launch_id}')
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def main():
    image_parser = argparse.ArgumentParser(
        description='''Program downloads pictures of SpaceX launches.
                    If no launch_id and path are given, the program will
                    download photo(s) from the last launch and place them
                    in the folder "images", located in the project directory.
                    If such a folder doesn't exist, it'll be created
                    automatically.'''
    )
    image_parser.add_argument('-l', '--launch_id', default='latest', type=str,
                              help='enter the launch id to download images.')
    image_parser.add_argument('-p', '--path', default=Path('images'),
                              help='enter path to save the image')
    args = image_parser.parse_args()
    check_create_path(Path(args.path))

    try:
        links_launch_images = get_links_to_photos(args.launch_id)
    except requests.exceptions.HTTPError:
        print('''You've entered incorrect "launch_id".''')
    if links_launch_images:
        image_quantity = len(links_launch_images)
        for url_id, url in enumerate(links_launch_images):
            flag = True
            try:
                response_image = requests.get(url)
                response_image.raise_for_status()
            except requests.exceptions.HTTPError:
                flag = False
                image_quantity -= 1
            if flag:
                save_image(response_image.content, Path(args.path),
                           '{}_{}'.format(
                    url_id, "".join(get_filename_extension(url))))
            elif not image_quantity:
                print(f"All links to images from {args.launch_id} launch",
                      "are invalid. Try to download images of another launch.")
    else:
        print(f"No pictures from {args.launch_id} launch.")


if __name__ == "__main__":
    main()
