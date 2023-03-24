import argparse
from api_tools import find_image_paths, publish_image_as_file
import os
import fetch_apod
from pathlib import Path


def is_photo_path(photo_path: Path) -> bool:
    if (os.path.isfile(photo_path) and
            os.path.splitext(photo_path)[-1] in ('.png', '.jpeg', '.jpg')):
        return True
    return False


def directory_contains_photo(direcory: Path) -> bool:
    if find_image_paths(direcory, image_quantity=1):
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="""The program publishes one picture from given path or
                       directory. But if the path isn't given program will
                       download APOD for the current day and publish it. After
                       publication picture would be deleted."""
    )
    parser.add_argument('-p', '--photo_path', default='images', type=Path,
                        help='''path to the directory with the photo to be
                        published''')
    args = parser.parse_args()
    if is_photo_path(args.photo_path):
        publish_image_as_file(args.args.photo_path)
        return
    elif directory_contains_photo(args.photo):
        publish_image_as_file(find_image_paths(args.photo_path))
        return
    fetch_apod.main()
    published_photo = find_image_paths(args.photo_path)
    publish_image_as_file(published_photo)
    os.remove(published_photo)
    print(f"The {published_photo} file was published and deleted after.")
    return


if __name__ == "__main__":
    main()
