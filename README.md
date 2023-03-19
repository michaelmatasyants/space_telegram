# Space Telegram

This project helps to find and download picture taken:
- During SpaceX launches;
- by NASA, which are called Astronomy Picture of The day (APOD);
- by NASA, using DSCOVR's Earth Polychromatic Imaging Camera (EPIC).

Using the scripts `fetch_apod.py`, `fetch_epic.py` and `fetch_spacex_images.py` scripts you can download images and put in the directory you desire.

You can also publish uploaded photos to your Telegram channel with the scripts `publish_1photo_tg.py` and `publish_all_photos_tg.py` using the bot you created.

### How to install

1. Firstly, you have to install python and pip (package-management system) if they haven't been already installed.

2. Create a virtual environment with its own independent set of packages using [virtualenv/venv](https://docs.python.org/3/library/venv.html). It'll help you to isolate the project from the packages located in the base environment.

3. Install all the packages used in this project, in your virtual environment which you've created on the step 2. Use the `requirements.txt` file to install dependencies:
    ```console
    pip install -r requirements.txt
    ```
4. Tokens and other keys:
   1. You need to [generate NASA API key](https://api.nasa.gov/) to access NASA API used in the `fetch_apod.py` and `fetch_epic.py` scripts. Be sure to save the resulting key.
   2. To publish images via `publish_1photo_tg.py` or `publish_all_photos_tg.py` script, you need to create a bot in Telegram. In order to do this, find `@BotFather` and start a new conversation with it. Then send him `/newbot` to create a new Telegram bot and follow the instructions. The last step will give you the bot's access Token, which you need to save.
   3. Enter the tg_chat_id of the channel (@example_channel) where you're going to publish photos using the bot, and don't forget to add the bot to the list of channel administrators.


5. Create an `.env` file and locate it in the same directory where your project is. Copy and append your access token to `.env` file like this:
    ```
    NASA_API_KEY=paste_here_your_token_from_step_4.1
    TG_BOT_TOKEN=paste_here_your_bot_token_from_step_4.2
    TG_CHAT_ID=paste_here_your_chanel_name_from_step_4.3
    ```
6. Remember to add `.env` to your `.gitignore` if you are going to put the project on GIT.

### Examples of running scripts

Before using each of the scripts `fetch_apod.py`, `fetch_epic.py`, `fetch_spacex_images.py`, `publish_1photo_tg.py` and `publish_all_photos_tg.py` it is recommended to run them with optional argument `-h` to read the description and explore the features of the programs.

Run in your console:
```Console
>>> python3 fetch_apod.py -h
```

Output:
```Console
usage: fetch_apod.py [-h] [-p PATH] [-d DATE] [-s START_DATE] [-e END_DATE]

Program downloads Astronomy Picture Of the Day (APOD). If no date (or start_date, end_date) and path are given, the program will download pictures of the curent day and place picture(s) in the folder "images", located in the project
directory. If such a folder doesn't exist, it'll be created automatically.

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  enter path to save the image
  -d DATE, --date DATE  enter date (YYYY-MM-DD) to download only 1 APOD
  -s START_DATE, --start_date START_DATE
                        enter start_date for period to download a few APOD
  -e END_DATE, --end_date END_DATE
                        enter end_date for period to download a few APOD
```
Each of the scripts individually:

1. The `fetch_apod.py` script downloads the picture(s) for the current day, specified day or period and places them in the given path. If such a path doesn't exist, it'll be created automatically:

    Download picture for the current day and place it in the directory `path/to/save/images/`:
    ```Console
    >>> python3 fetch_apod.py -p path/to/save/images/
    ```

    Download the picture for 2021/01/18 and put it in the `path/to/save/images/` directory:
    ```Console
    >>> python3 fetch_apod.py -d 2021-01-18 -p path/to/save/images/
    ```

    Download photos taken from 2020/01/15 through 2020/01/18 and place them in the folder `images`, located in the project directory. Remember, if such a folder doesn't exist, it'll be created automatically:
    ```Console
    >>> python3 fetch_apod.py -s 2020-01-15 -e 2020-01-18
    ```

2. The `fetch_epic.py` script downloads natural color images of the Earth and puts them in a directory at the given path. If you don't specify an image extension and a path to save, the program will download image(s) with "PNG" extension and place them in the "images" folder located in the project directory. If such a folder doesn't exist, it'll be created automatically.

    Download the picture for current day and put it in the directory `path/to/save/images/`:
    ```Console
    >>> python3 fetch_epic.py -p path/to/save/images/
    ```

3. The `fetch_spacex_images.py` script downloads pictures of SpaceX launches. If no launch_id and path are given, the program will download photo(s) from the last launch and place them in the folder "images", located in the project directory. If such a folder doesn't exist, it'll be created automatically.

    Download images from the last launch and put it in the `path/to/save/images/` directory:
    ```Console
    >>> python3 fetch_spacex_images.py -p path/to/save/images/
    ```

    Download pictures from the launch_id `5eb87d42ffd86e000604b384` and place them in the `path/to/save/images/` directory:
    ```Console
    >>> python3 fetch_spacex_images.py -i 5eb87d42ffd86e000604b384 -p path/to/save/images/
    ```

4. The `publish_1photo_tg.py` script publishes one photo from the specified directory path. If the path isn't given, the program will download APOD for the current day and publish it. After publishing, the picture will be deleted from the PC.

    Post the photo to the Telegram channel by specifying the photo path `enter/the/path/to/the/photo.png` (сhat_id of the channel must be set in the `.env` file.):

    ```Console
    >>> python3 publish_1photo_tg.py -p enter/the/path/to/the/photo.png
    ```

    Post photo APOD for current day in the Telegram channel (tg_chat_id of the channel must be set in the `.env` file.):
    ```Console
    >>> python3 publish_1photo_tg.py
    ```

5. The `publish_all_photos_tg.py` script publishes all photos from a given directory path at a fixed interval, every 4 hours (by default). You can also loop publish photos from directory and subdirectories. After first publishing of all images, they will be shuffled to publish them in a different order.

    Post all the photos located in the `enter/the/path/to/the/images` directory and set frequency of publication as every 6 hours:
    ```Console
    >>> python3 publish_all_photos_tg.py enter/the/path/to/the/images -f 6
    ```

    Post all the photos located in the `enter/the/path/to/the/images` directory and subdirectories. Loop publish photos until the script wouldn't be soped.
    ```Console
    >>> python3 publish_all_photos_tg.py enter/the/path/to/the/images -e
    ```

### Project Goals
The code is written for educational purposes.
