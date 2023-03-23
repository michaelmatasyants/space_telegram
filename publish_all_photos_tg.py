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
    paths_to_publish_photos = api_tools.find_paths_to_images(
        args.photo_path, count_of_images="all")
    time_to_sleep = args.frequency * 3600
    if args.endless:
        first_network_error = True
        while True:
            for photo_path in paths_to_publish_photos:
                try:
                    api_tools.publish_image_as_file(photo_path)
                except telegram.error.NetworkError:
                    if first_network_error:
                        first_network_error, time_to_sleep = False, 5
                finally:
                    time.sleep(time_to_sleep)
            shuffle(paths_to_publish_photos)
    else:
        for photo_path in paths_to_publish_photos:
            api_tools.publish_image_as_file(photo_path)
            time.sleep(time_to_sleep)


if __name__ == "__main__":
    main()
