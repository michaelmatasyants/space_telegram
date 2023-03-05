import argparse
import spacex_nasa_api
import os
import fetch_apod


def find_image(path_to_search):
    for root, dirs, files in os.walk(path_to_search):
        for file in files:
            if file.endswith(('.png', '.jpeg', '.jpg')):
                return f'{root}/{file}'


def main():
    parser = argparse.ArgumentParser(
        description="""The program publishes one picture from given directory
                    path. But if the path isn't given programm will download
                    APOD for the curent day and publish it. After publication
                    picture would be deleted."""
    )
    parser.add_argument('-p', '--photo_path', default=None,
                        help='''path to the directory with the photo to be
                        published''')
    args = parser.parse_args()
    if (args.photo_path is None) or (
        not os.path.isfile(args.photo_path) and
        os.path.splitext(args.photo_path)[-1] not in ('.png', '.jpeg', '.jpg')
    ):
        fetch_apod.main()
        photo_to_publish = find_image(os.path.expanduser("~"))
        spacex_nasa_api.publish_image_as_file(photo_to_publish)
        os.remove(photo_to_publish)
        print(f"The {photo_to_publish} file was published and deleted after")
    else:
        spacex_nasa_api.publish_image_as_file(args.photo_path)


if __name__ == "__main__":
    main()
