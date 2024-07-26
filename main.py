from telebot import TeleBot, types
import config
import random
import message

bot = TeleBot(config.BOT_TOKEN)
message_help = message.help_message
known_joke = message.UNKNOWN_JOKES
message_start = message.start_message
@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(message.chat.id, random.choice(known_joke))

@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(message.chat.id, message_start)

@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(message.chat.id, message_help)

@bot.message_handler()
def send_some_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'Привет! Как ты?'
    elif 'дела' in text.lower():
        text = 'Нормально!'
    bot.send_message(message.chat.id, text)

#Проверка, для запуска именно этого файла
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)