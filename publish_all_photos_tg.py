import os
import argparse
import time
from pathlib import Path
from random import shuffle
from dotenv import load_dotenv, find_dotenv
import telegram
import api_tools


def post_photos(all_photo_paths: list, sleep_time: float,
                bot_token: str, chat_id: str):
    for photo_path in all_photo_paths:
        api_tools.publish_image_as_file(photo_path, bot_token, chat_id)
        time.sleep(sleep_time)


def post_nonstop_photos(all_photo_paths: list, post_frequency: float,
                        bot_token: str, chat_id: str):
    first_network_error = True
    while True:
        try:
            post_photos(all_photo_paths, bot_token=bot_token, chat_id=chat_id,
                        sleep_time=post_frequency)
        except telegram.error.NetworkError:
            if first_network_error:
                first_network_error, sleep_time = False, 5
            time.sleep(sleep_time)
        shuffle(all_photo_paths)


def main():
    load_dotenv(find_dotenv())
    bot_token, chat_id = os.environ['TG_BOT_TOKEN'], os.environ['TG_CHAT_ID']
    parser = argparse.ArgumentParser(
        description='''The program publishes all pictures from given directory
                    path at fixed interval, every 4 hours (by default).
                    If you want to continue publishing pictures, after they
                    have all been published until you stop, set '--endless'
                    or '-e' optional argument.'''
    )
    parser.add_argument('-p', '--photo_path', default='images', type=Path,
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
        post_photos(published_photo_paths, sleep_time, bot_token, chat_id)
        return
    print("Press 'Ctrl + C' to stop the script.")
    post_nonstop_photos(published_photo_paths, sleep_time, bot_token, chat_id)


if __name__ == "__main__":
    main()
