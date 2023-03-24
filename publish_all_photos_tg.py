import argparse
import api_tools
import time
from random import shuffle
from pathlib import Path
import telegram


def post_photos(all_photo_paths: list, sleep_time: float):
    for photo_path in all_photo_paths:
        api_tools.publish_image_as_file(photo_path)
        time.sleep(sleep_time)


def post_nonstop_photos(all_photo_paths: list, post_frequency: float):
    sleep_time = post_frequency
    first_network_error = True
    while True:
        try:
            post_photos(all_photo_paths, sleep_time)
        except telegram.error.NetworkError:
            if first_network_error:
                first_network_error, sleep_time = False, 5
            time.sleep(sleep_time)
        shuffle(all_photo_paths)


def main():
    parser = argparse.ArgumentParser(
        description='''The program publishes all pictures from given directory
                    path at fixed interval, every 4 hours (by default).
                    If you want to continue publishing pictures, after they
                    have all been published until you stop, set '--endless'
                    or '-e' optional argument.'''
    )
    parser.add_argument('photo_path', type=Path,
                        help='''path to the directory with the
                        photos to be published''')
    parser.add_argument('-f', '--frequency', default=4, type=float,
                        help='''frequency of publishing photos on Telegram
                        (once every 'X' hours)''')
    parser.add_argument('-e', '--endless', action="store_true",
                        help='start endless publishing')
    args = parser.parse_args()
    sleep_time = args.frequency * 3600
    published_photo_paths = api_tools.find_image_paths(args.photo_path,
                                                       image_quantity="all")
    if not args.endless:
        post_photos(published_photo_paths, sleep_time)
        return
    if args.endless:
        print("Press 'Ctrl + C' to stop the script.")
        post_nonstop_photos(published_photo_paths, sleep_time)


if __name__ == "__main__":
    main()
