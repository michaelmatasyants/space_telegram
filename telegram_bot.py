import telegram
import spacex_nasa_api


def publish_message(text):
    bot = telegram.Bot(token=spacex_nasa_api.get_api_key()['tg_api_key'])
    bot.send_message(chat_id=spacex_nasa_api.get_api_key()['chat_id'],
                     text=text)


def publish_image_as_file(photo_path):
    bot = telegram.Bot(token=spacex_nasa_api.get_api_key()['tg_api_key'])
    bot.send_document(chat_id=spacex_nasa_api.get_api_key()['chat_id'],
                      document=open(photo_path, 'rb'))