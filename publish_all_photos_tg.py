import argparse
import spacex_nasa_api
import time
from random import shuffle
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='''The program publishes all pictures from given directory
                    path at fixed interval, every 4 hours (by default).
                    If you want to continue publishing pictures, after they
                    have all been published until you stop, set '--endless'
                    or '-e' optional argument.'''
    )
    parser.add_argument('photo_path', help='''path to the directory with the
                        photos to be published''')
    parser.add_argument('-f', '--frequency', default=4, type=float,
                        help='''frequency of publishing photos on Telegram
                        (once every 'X' hours)''')
    parser.add_argument('-e', '--endless', action="store_true",
                        help='start endless publishing')
    args = parser.parse_args()
    paths_to_publish_photos = spacex_nasa_api.find_paths_to_images(
        Path(args.photo_path), count_of_images="all")
    for photo_path in paths_to_publish_photos:
        spacex_nasa_api.publish_image_as_file(photo_path)
        time.sleep(args.frequency * 3600)
    while args.endless:
        shuffle(paths_to_publish_photos)
        for photo_path in paths_to_publish_photos:
            spacex_nasa_api.publish_image_as_file(photo_path)
            time.sleep(args.frequency * 3600)


if __name__ == "__main__":
    main()
