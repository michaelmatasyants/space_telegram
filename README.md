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
   2. To publish images via `publish_1photo_tg.py` or `publish_all_photos_tg.py` script you need to create a bot in Telegram. In order to do this, find `@BotFather` and start a new conversation with it. Then send him `/newbot` to create
   a new Telegram bot and follow the instructions. The last step will give you the bot's access Token, which you need to save. 
   3. Enter the chat_id of the channel (@example_channel) where you're going to publish photos using the bot, and don't forget to add the bot to the list of channel administrators.


5. Create an `.env` file and locate it in the same directory where your project is. Copy and append your access token to `.env` file like this:
    ```
    NASA_API_KEY=paste_here_your_token_from_step_4.1
    TG_TOKEN=paste_here_your_bot_token_from_step_4.2
    CHAT_ID=paste_here_your_chanel_name_from_step_4.3
    ```
6. Remeber to add `.env` to your `.gitignore` if you are going to put the project on GIT.


### Project Goals
The code is written for educational purposes.