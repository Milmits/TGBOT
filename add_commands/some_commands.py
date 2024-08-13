import random

from telebot import types, TeleBot

import messagepy


def answer_command_start(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, messagepy.start_message)


def answer_help_command(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        messagepy.help_message
    )


def give_random_joke(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, random.choice(messagepy.UNKNOWN_JOKES))
