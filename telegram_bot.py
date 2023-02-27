import telegram
from spacex_nasa_api import get_api_key


def main():
    bot = telegram.Bot(token=get_api_key()['tg_api_key'])
    updates = bot.get_updates()
    CHAT_ID = updates[0]['channel_post']['chat']['id']
    text_to_publish = 'Fist message published by bot'
    bot.send_message(text=text_to_publish, chat_id=CHAT_ID)


if __name__ == '__main__':
    main()