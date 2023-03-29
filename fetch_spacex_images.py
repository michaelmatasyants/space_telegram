from pathlib import Path
import argparse
import requests
from api_tools import download_all_images, check_create_path


def get_links_to_all_photos(launch_id: str) -> list:
    response = requests.get(
        f'https://api.spacexdata.com/v5/launches/{launch_id}')
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
    image_parser.add_argument('-p', '--path', default='images', type=Path,
                              help='enter path to save the image')
    args = image_parser.parse_args()
    check_create_path(args.path)

    try:
        launch_image_links = get_links_to_all_photos(args.launch_id)
    except requests.exceptions.HTTPError:
        print('''You've entered incorrect "launch_id".''')
        return
    if not launch_image_links:
        print(f"No pictures from {args.launch_id} launch.")
        return

    downloaded_image_names = download_all_images(
        launch_image_links, args.path,
        added_to_the_top_of_image_name=args.launch_id
        )
    if not downloaded_image_names:
        print(f"All links to images from {args.launch_id} launch",
              "are invalid. Try to download images of another launch.")
        return
    print(*downloaded_image_names, sep=', ', end=' ')
    print(f'successfully downloaded to {args.path}.')


if __name__ == "__main__":
    main()
