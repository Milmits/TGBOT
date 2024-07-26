from telebot import TeleBot, types
import config
import random
import messagepy

bot = TeleBot(config.BOT_TOKEN)
@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(message.chat.id, random.choice(messagepy.UNKNOWN_JOKES))

@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(message.chat.id, messagepy.start_message)

@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(message.chat.id, messagepy.help_message)
@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: types.Message):
    bot.send_message(message.chat.id, "Классный стикер!", reply_to_message_id=message.id)

@bot.message_handler(content_types=["photo"])
def handle_photo(message: types.Message):
    photo_file_id = message.photo[-1].file_id
    bot.send_photo(message.chat.id, photo_file_id, reply_to_message_id=message.id)
    with open('wolf.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
@bot.message_handler(content_types=["voice"])
def handle_voice(message: types.Message):
    bot.send_message(message.chat.id, "К сожалению я не могу прослушать что вы сказали :(", reply_to_message_id=message.id)
@bot.message_handler()
def send_some_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'Привет! Как ты?'
    elif 'как дела' in text.lower():
        text = 'Нормально!'
    elif 'пока' in text.lower() or 'до свидания' in text.lower():
        text = 'До новых встреч!'
    bot.send_message(message.chat.id, text)

#Проверка, для запуска именно этого файла
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)

