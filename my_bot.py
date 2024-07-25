from telebot import TeleBot, types
import config
import random

M = 'for commit'

bot = TeleBot(config.BOT_TOKEN)

help_message = """Привет, Доступные команды:
    /start - начало работы с ботом
    /help - помощь (это сообщение)
    /joke - случайная шутка xD
    
Этот бот отправит вам то же сообщение, что и вы ему!
"""

UNKNOWN_JOKES = [
    ("Завтра буду спать до 12 дня.\n(Запись понравилась 15 газонокосильщикам)"),
    'Выспался? Уже неплохо. Не надо ждать от жизни многого.',
    'Легче всего встается по будильнику в день зарплаты.',
    'Не будет шутки, я устал!!!'
]
@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(message.chat.id, random.choice(UNKNOWN_JOKES))

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



bot.infinity_polling(skip_pending=True)