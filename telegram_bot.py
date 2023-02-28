import telegram
from spacex_nasa_api import get_api_key


def publish_message(text):
    bot = telegram.Bot(token=get_api_key()['tg_api_key'])
    updates = bot.get_updates()
    chat_id = updates[0]['channel_post']['chat']['id']
    bot.send_message(chat_id=chat_id, text=text)


def publish_image_as_file(photo_path):
    bot = telegram.Bot(token=get_api_key()['tg_api_key'])
    updates = bot.get_updates()
    chat_id = updates[0]['channel_post']['chat']['id']
    bot.send_document(chat_id=chat_id, document=open(photo_path, 'rb'))
