# from main import Bot
from telebot.types import Message


class Channel:

    def __init__(self, id, title) -> None:
        self.id = id
        self.title = title


def add_channel(message: Message, bot: 'Bot'):
    channel = message.forward_from_chat
    if channel:
        if channel.id in map(lambda x: x.id, bot.users_channels[message.from_user.id]):
            msg = bot.send_message(message.chat.id, f'The channel {message.forward_from_chat.title} is already in your list!')
        else:
            bot.users_channels[message.from_user.id].append(Channel(channel.id, channel.title))
            msg = bot.send_message(message.chat.id, f'The channel {channel.title} has been sucessfully added to your list!')
    else:
        msg = bot.send_message(message.chat.id, 'This is not a forwarded message from another chat!')


def remove_channel(message: Message, bot: 'Bot'):
    channel = message.forward_from_chat
    if channel:
        if channel.id not in map(lambda x: x.id, bot.users_channels[message.from_user.id]):
            msg = bot.send_message(message.chat.id, f'The channel {message.forward_from_chat.title} is not in your list!')
        else:
            for chnl in bot.users_channels[message.from_user.id]:
                if chnl.id == channel.id:
                    bot.users_channels[message.from_user.id].remove(chnl)
                    break
            msg = bot.send_message(message.chat.id, f'The channel {channel.title} has been sucessfully removed from your list!')
    else:
        msg = bot.send_message(message.chat.id, 'This is not a forwarded message from another chat!')