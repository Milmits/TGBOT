#библиотека для работы с tg ботом
from telebot import TeleBot, types

import config
import random
import messagepy

#библиотека input, output для работы с файлами
from io import StringIO, BytesIO

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

#Команды менюшки_6
#Отправка пользователю фото по id картинки
@bot.message_handler(commands=["sunrise_by_id"])
def send_sunrise_picture_by_file_id(message: types.Message):
    bot.send_photo(message.chat.id, photo=config.SUNRISE_PIC_FILE_ID)

#Команды менюшки_7
#Отправка пользователю фото как документ
@bot.message_handler(commands=["sunrise_doc"])
def send_sunrise_doc(message: types.Message):
    photo_file = types.InputFile('pics/sunrise-pic.jpg')
    bot.send_document(chat_id=message.chat.id, document=photo_file)

#Команды менюшки_8
#Отправка пользователю фото как документ по id картинки
@bot.message_handler(commands=["wolf_doc_id"])
def send_wolf_doc_by_id(message: types.Message):
    bot.send_document(chat_id=message.chat.id, document=config.WOLF_photo)

#Команды менюшки_9
#Отправка пользователю файла, который находится в нашей дерректории
@bot.message_handler(commands=["file_txt"])
def send_file_txt(message: types.Message):
    file_doc = types.InputFile('text.txt')
    bot.send_document(chat_id=message.chat.id, document=file_doc)

#Команды менюшки_10
#Отправка пользователю файла, который находится на нашем pc
@bot.message_handler(commands=["text"])
def send_text_doc_from_memory(message: types.Message):
    file = StringIO("Приветики)))")
    file.write("Hello peoples!!!\n")
    file.write("Random number\n")
    file.write(str(random.randint(1, 1000)))
    file.seek(0)
    file_text_doc = types.InputFile(file)
    bot.send_document(chat_id=message.chat.id, document=file_text_doc, visible_file_name="yor_file_from_pc.txt")

#----------------------------------------------------------------------------

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
