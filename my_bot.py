from telebot import TeleBot, types

TOKEN = '7240943425:AAGlCcMDrbJhkZV7FpIFtZ8Yd5buyabJ7RY'

bot = TeleBot(TOKEN)


text = 'Привет, извини, но я пока приостановлен, надеюсь в скором времени меня вновь запустят...'

@bot.message_handler()
def send_some_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'Привет! Как ты?'
    if 'дела' in text.lower():
        text = 'Все супер!'
    bot.send_message(message.chat.id, text)



bot.infinity_polling()