import telegram
from spacex_nasa_api import get_api_key


def main():
    bot = telegram.Bot(token=get_api_key()['tg_api_key'])
    updates = bot.get_updates()
    chat_id = updates[0]['channel_post']['chat']['id']
    bot.send_message(chat_id=chat_id, text='Fist message published by bot')
    bot.send_document(chat_id=chat_id, document=open(
        './images/spacex_0.jpg', 'rb'
        ))


if __name__ == '__main__':
    main()
