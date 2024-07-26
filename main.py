from telebot import TeleBot, types
import config
import random
import messagepy

bot = TeleBot(config.BOT_TOKEN)

#Команды менюшки_1
@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(message.chat.id, random.choice(messagepy.UNKNOWN_JOKES))
#Команды менюшки_2
@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(message.chat.id, messagepy.start_message)
#Команды менюшки_3
@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(message.chat.id, messagepy.help_message)
# Команды менюшки_4
@bot.message_handler(commands=["wolf"])
def send_wolf_photo(message: types.Message):
    bot.send_photo(message.chat.id, photo=config.WOLF_photo, reply_to_message_id=message.id)

#Команды менюшки_5
#Отправка пользователю фото в виде файла
@bot.message_handler(commands=["sunrise_file"])
def send_sunrise_photo_from_disk(message: types.Message):
    photo_file = types.InputFile('pics/sunrise-pic.jpg')
    msg = bot.send_photo(message.chat.id, photo=photo_file)

#Команды менюшки_5
#
@bot.message_handler(commands=["sunrise_by_id"])
def send_sunrise_picture_by_file_id(message: types.Message):
    bot.send_photo(message.chat.id, photo=config.SUNRISE_PIC_FILE_ID)



#Реакция на событие - отправка стикера
@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: types.Message):
    bot.send_message(message.chat.id, "Классный стикер!", reply_to_message_id=message.id)

#Реакция на событие - реакция на подпись под картинкой "волк" (1)
def is_wolf_in_caption(message: types.Message):
    return message.caption and "волк" in message.caption.lower()

#Реакция на событие - реакция на подпись под картинкой "волк" (2)
@bot.message_handler(content_types=["photo"], func=is_wolf_in_caption)
def handle_photo_with_wolf_caption(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text='Nice photo!', reply_to_message_id=message.id)

# Реакция на событие - дублируем последнее фото без подписи
@bot.message_handler(content_types=["photo"])
def handle_photo(message: types.Message):
    photo_file_id = message.photo[-1].file_id
    caption_text = 'Классное фото!'
    if message.caption:
        caption_text += "\nПодпись:\n" + message.caption
    bot.send_photo(message.chat.id, photo=photo_file_id, reply_to_message_id=message.id, caption=caption_text)

# Реакция на событие - голосовое сообщение
@bot.message_handler(content_types=["voice"])
def handle_voice(message: types.Message):
    bot.send_message(message.chat.id, "К сожалению я не могу прослушать что вы сказали :(", reply_to_message_id=message.id)

# Реакция на событие - ответ если определенные слова есть в сообщении пользователя
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
