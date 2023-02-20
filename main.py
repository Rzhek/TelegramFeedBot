import telebot
from dotenv import load_dotenv
import os


class Bot(telebot.TeleBot):
    
    def __init__(self, token):
        super().__init__(token)


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot = Bot(TOKEN)

    @bot.message_handler(content_types=['text'])
    def reply(message):
        bot.send_message(message.from_user.id, message.text)

    bot.polling(non_stop=True, interval=0)