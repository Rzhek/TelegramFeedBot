from typing import Dict, List
import telebot
from dotenv import load_dotenv
import os

from handlers import add_channel, remove_channel
from collections import defaultdict

# TODO: Make the bot watch added channels and forward new messages to users
# TODO: Change the method of storing users' data from dictionary to database
# TODO: Organize the code: move methods to correct classes and files, inlcude types of vatiables
class Bot(telebot.TeleBot):
    
    def __init__(self, token):
        super().__init__(token)
        self.users_channels = defaultdict(list)


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot = Bot(TOKEN)

    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        bot.send_message(
            message.from_user.id,
            f"Hi {message.from_user.username}! I'm a telegram bot that can make you forget about watching thousands of your channels individually!\n\
            You can watch all news from your channels in a single chat.\n\
            But before we do that, you need to add those channels to your personal list.\n\n\
            To see all your connected channels, use /list command\n\
            To add a new channel to your list, use /add command\n\
            To remove a channel from your list, use /remove command\
            ".replace("  ", "")
        )
    
    @bot.message_handler(commands=['list'])
    def list(message):
        if len(bot.users_channels[message.from_user.id]) == 0:
            bot.send_message(message.from_user.id, f"You don't have any channels added to your list! Please use the /add command to add them!")
            return
        
        msg = 'Your channels:\n\n'
        for channel in bot.users_channels[message.from_user.id]:
            msg += f'{channel.title}\n'
        bot.send_message(message.from_user.id, msg)

    @bot.message_handler(commands=['add'])
    def add(message):
        msg = bot.send_message(message.from_user.id, f"Please forward the message from the channel you want to add to this chat")
        bot.register_next_step_handler(msg, add_channel, bot=bot)
    
    @bot.message_handler(commands=['remove'])
    def remove(message):
        msg = bot.send_message(message.from_user.id, f"Please forward the message from the channel you want to remove from this chat")
        bot.register_next_step_handler(msg, remove_channel, bot=bot)

    @bot.message_handler(content_types=['text'])
    def reply(message):
        print(bot.users_channels)
        bot.send_message(message.from_user.id, message.text)

    bot.polling(non_stop=True, interval=0)