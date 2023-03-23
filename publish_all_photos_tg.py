import argparse
import api_tools
import time
from random import shuffle
from pathlib import Path
import telegram


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
    published_photo_paths = api_tools.find_image_paths(
        args.photo_path, image_quantity="all")
    sleep_time = args.frequency * 3600
    if args.endless:
        first_network_error = True
        while True:
            for photo_path in published_photo_paths:
                try:
                    api_tools.publish_image_as_file(photo_path)
                except telegram.error.NetworkError:
                    if first_network_error:
                        first_network_error, sleep_time = False, 5
                finally:
                    time.sleep(sleep_time)
            shuffle(published_photo_paths)
    else:
        for photo_path in published_photo_paths:
            api_tools.publish_image_as_file(photo_path)
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()
