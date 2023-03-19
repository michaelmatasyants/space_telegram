import argparse
import spacex_nasa_api
import os
import fetch_apod
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="""The program publishes one picture from given directory
                    path. But if the path isn't given programm will download
                    APOD for the curent day and publish it. After publication
                    picture would be deleted."""
    )
    parser.add_argument('-p', '--photo_path', default=Path('images'),
                        help='''path to the directory with the photo to be
                        published''')
    args = parser.parse_args()
    if (args.photo_path == Path('images') or
        not os.path.isfile(Path(args.photo_path)) or
        os.path.splitext(Path(args.photo_path))[-1] not in (
            '.png', '.jpeg', '.jpg'
            )):
        fetch_apod.main()
        photo_to_publish = spacex_nasa_api.find_paths_to_images(
            args.photo_path)
        spacex_nasa_api.publish_image_as_file(photo_to_publish)
        os.remove(photo_to_publish)
        print(f"The {photo_to_publish} file was published and deleted after")
    else:
        spacex_nasa_api.publish_image_as_file(Path(args.photo_path))


if __name__ == "__main__":
    main()
