from telebot import TeleBot, types

TOKEN = '7240943425:AAGlCcMDrbJhkZV7FpIFtZ8Yd5buyabJ7RY'

bot = TeleBot(TOKEN)

help_message = """Привет, Доступные команды:
    /start - начало работы с ботом
    /help - помощь (это сообщение)
    /joke - случайная шутка xD
Этот бот отправит вам то же сообщение, что и вы ему!
"""
@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(message.chat.id, 'Привет, давай знакомиться!!')

@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(message.chat.id, help_message)
@bot.message_handler()
def send_some_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'Привет! Как ты?'
    elif 'дела' in text.lower():
        text = 'Нормально!'
    bot.send_message(message.chat.id, text)



bot.infinity_polling()