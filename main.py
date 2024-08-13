#библиотека для работы с tg ботом
from telebot import TeleBot
from telebot import custom_filters
#библиотека input, output для работы с файлами
from io import StringIO
#библиотека для форматирования текста
from telebot import formatting
#библиотеки для конвертации валют
from telebot import util
from telebot import types
#добавляем команды
from commands import default_commands
#Кэширование информации о доступных валютах
from functools import lru_cache
from datetime import datetime, timedelta

import os
import requests
import config
import random
import messagepy
from custom_filters import my_filters
import re
import json


#для кэширования данных
#--------------------------------------------------------------------------------------------
# Время жизни кэша
CACHE_EXPIRATION_DAYS = 1

# Декоратор для сброса кэша
def cache_with_expiration(expiration_days: int):
    def decorator(func):
        cache = lru_cache(maxsize=128)(func)
        cache.expiration_date = datetime.now() + timedelta(days=expiration_days)

        def wrapped_func(*args, **kwargs):
            if datetime.now() > cache.expiration_date:
                cache.cache_clear()
                cache.expiration_date = datetime.now() + timedelta(days=expiration_days)
            return cache(*args, **kwargs)

        return wrapped_func

    return decorator


@cache_with_expiration(CACHE_EXPIRATION_DAYS)
def get_available_currencies(api_key):
    # Функция для получения списка доступных валют
    # Здесь должен быть запрос к API или другим источникам данных
    return ["USD", "EUR", "GBP", "JPY", "RUB", "IDR", "INR"]


#Создание файла для хранения пользовательских валют:
#--------------------------------------------------------------------------------------------
USER_CURRENCIES_FILE = "user_currencies.json"
currency_code_pattern = re.compile(r'^[A-Z]{3}$')

def load_user_currencies():
    if os.path.exists(USER_CURRENCIES_FILE):
        with open(USER_CURRENCIES_FILE, "r") as file:
            return json.load(file)
    return {}

def save_user_currencies(user_currencies):
    with open(USER_CURRENCIES_FILE, "w") as file:
        json.dump(user_currencies, file)

user_currencies = load_user_currencies()
#--------------------------------------------------------------------------------------------

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextContainsFilter())
bot.add_custom_filter(my_filters.IsUserBotAdmin())
bot.add_custom_filter(my_filters.ContainsWordFilter())


#Для получения актуальной информации об конвертации валют
def get_exchange_rate(api_key: str, from_currency: str, to_currency: str) -> float:
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if to_currency in data['conversion_rates']:
            return data['conversion_rates'][to_currency]
        else:
            raise ValueError(f"Неподдерживаемая валюта: {to_currency}")
    else:
        raise ValueError("Не удалось получить данные о курсе валют.")


# Генерация клавиатуры для выбора валюты
def generate_currency_keyboard(user_id=None, selected_currency=None):
    markup = types.InlineKeyboardMarkup(row_width=4)
    default_currencies = ["USD", "EUR", "TRY", "BYN", "RUB", "PLN"]
    user_specific_currencies = user_currencies.get(str(user_id), [])
    currencies = list(set(default_currencies + user_specific_currencies))

    buttons = [types.InlineKeyboardButton(
        text=cur, callback_data=f"select_currency:{cur}") for cur in currencies]
    markup.add(*buttons)

    # Если выбрана валюта, добавьте кнопку для сброса выбора
    if selected_currency:
        reset_button = types.InlineKeyboardButton(
            text="Сбросить выбор",
            callback_data="reset_currency"
        )
        markup.add(reset_button)

    return markup

# Обработчик команды для конвертации валюты
@bot.message_handler(commands=["cvt"])
def currency_conversion(message: types.Message):
    selected_currency = user_currencies.get(str(message.from_user.id), None)
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите валюту, из которой хотите конвертировать:",
        reply_markup=generate_currency_keyboard(message.from_user.id, selected_currency)
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_currency_selection(call: types.CallbackQuery):
    callback_data = call.data
    user_id = call.from_user.id

    if callback_data.startswith("select_currency:"):
        # Обработка выбора валюты
        selected_currency = callback_data.split(":")[1]
        user_currencies[str(user_id)] = selected_currency
        save_user_currencies(user_currencies)

        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Вы выбрали {selected_currency}. Введите сумму и валюту для конвертации в формате: 100 {selected_currency} TO EUR или введите другую валюту:",
        )
        bot.register_next_step_handler(msg, process_amount_step, selected_currency)

    elif callback_data == "reset_currency":
        # Сброс выбора валюты
        if str(user_id) in user_currencies:
            del user_currencies[str(user_id)]
            save_user_currencies(user_currencies)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выбор валюты сброшен. Выберите валюту для конвертации снова.",
            reply_markup=generate_currency_keyboard(user_id)
        )
# Обработка ввода суммы и валюты для конвертации
def process_amount_step(message: types.Message, from_currency: str):
    try:
        if message.text.strip().lower() == 'exit':
            bot.send_message(chat_id=message.chat.id, text="Операция отменена.")
            return

        match = re.match(r"(\d+(?:\.\d+)?)\s+" + re.escape(from_currency) + r"\s+TO\s+(\w+)", message.text, re.IGNORECASE)
        if match:
            amount_str, to_currency = match.groups()
            amount = float(amount_str)
            exchange_rate = get_exchange_rate(config.EXCHANGERATE_API_KEY, from_currency, to_currency.upper())
            converted_amount = amount * exchange_rate
            result_text = (
                f"{formatting.hcode(str(amount))} {formatting.hcode(from_currency)} = "
                f"{formatting.hcode(f'{converted_amount:.2f}')} {formatting.hcode(to_currency.upper())}"
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=result_text,
                parse_mode="HTML"
            )
        else:
            raise ValueError(" ")
    except ValueError as e:
        if "Неподдерживаемая валюта" in str(e):
            msg = bot.send_message(
                chat_id=message.chat.id,
                text=f"Ошибка: {formatting.hcode(str(e))}. Пожалуйста, введите сумму и валюту для конвертации снова в формате: | 100 {from_currency} TO EUR |, "
                     f"вы также можете выбрать другую валюту как: | 100 {from_currency} TO 'ваша валюта' | или 'exit' для выхода:"
            )
        else:
            msg = bot.send_message(
                chat_id=message.chat.id,
                text=f"Ошибка: {formatting.hcode(str(e))}. Похоже вы используете неподдерживаемую валюту, "
                     f"завершите операцию 'exit' и попробуйте снова:"
            )
        bot.register_next_step_handler(msg, process_amount_step, from_currency)
    except Exception as e:
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=f"Произошла ошибка: {formatting.hcode(str(e))}. Пожалуйста, попробуйте снова или введите 'exit' для выхода.")

# Обработчик inline-запросов для конвертации валют
@bot.inline_handler(func=lambda query: query.query.strip().isdigit() or query.query.lower().startswith("exchange"))
def handle_convert_inline_query(query: types.InlineQuery):
    try:
        user_id = query.from_user.id
        amount_str = query.query.strip()
        amount = float(amount_str) if amount_str.isdigit() else 0

        from_currency = user_currencies.get(str(user_id), "USD")  # Используйте валюту пользователя или по умолчанию USD

        target_currencies = ["USD", "EUR", "TRY", "BYN", "RUB", "PLN"]  # Добавьте нужные вам валюты

        results = []

        for to_currency in target_currencies:
            exchange_rate = get_exchange_rate(config.EXCHANGERATE_API_KEY, from_currency, to_currency)
            converted_amount = amount * exchange_rate

            result_text = (
                f"{formatting.hcode(str(amount))} {formatting.hcode(from_currency)} = "
                f"{formatting.hcode(f'{converted_amount:.2f}')} {formatting.hcode(to_currency)}"
            )

            result = types.InlineQueryResultArticle(
                id=to_currency,
                title=f"{amount} {from_currency} в {to_currency}",
                input_message_content=types.InputTextMessageContent(
                    message_text=result_text,
                    parse_mode="HTML"
                ),
                description=result_text
            )

            results.append(result)

        bot.answer_inline_query(query.id, results, cache_time=5)

    except Exception as e:
        bot.answer_inline_query(query.id, results=[], cache_time=5)
        print(f"Ошибка в обработке inline запроса: {e}")



#Для прогноза погоды в реальном времени
def get_weather(city: str, api_key: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        return (f"Погода в {city}:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature}°C\n"
                f"Ощущается как: {feels_like}°C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с")
    else:
        return "Не удалось получить данные о погоде."

# Команды менюшки_1
@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(message.chat.id, random.choice(messagepy.UNKNOWN_JOKES))


# Команды менюшки_2
@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(message.chat.id, messagepy.start_message)


# Команды менюшки_3
@bot.message_handler(commands=["help"])
def handle_command_help(message: types.Message):
    bot.send_message(message.chat.id, messagepy.help_message)


# Команды менюшки_4
@bot.message_handler(commands=["wolf"])
def send_wolf_photo(message: types.Message):
    bot.send_photo(message.chat.id,
                   photo=config.WOLF_photo,
                   reply_to_message_id=message.id)


# Команды менюшки_5
# Отправка пользователю фото в виде файла
@bot.message_handler(commands=["sunrise_file"])
def send_sunrise_photo_from_disk(message: types.Message):
    photo_file = types.InputFile('pics/sunrise-pic.jpg')
    msg = bot.send_photo(message.chat.id, photo=photo_file)


# Команды менюшки_6
# Отправка пользователю фото по id картинки
@bot.message_handler(commands=["sunrise_id"])
def send_sunrise_photo_by_id(message: types.Message):
    photo_id = "AgACAgIAAxkBAAMrZFFg2CeNwZZMS-...HhVLsd6Y-LyAAgvM"
    bot.send_photo(message.chat.id, photo=photo_id)

#---------------------------------------------------------------------
# Бот для работы с фото и аудио файлами
@bot.message_handler(content_types=["photo", "audio"])
def echo_photo_or_audio(message: types.Message):
    if message.content_type == "photo":
        bot.reply_to(message, f"Фото {message.photo[-1].file_id} добавлено успешно!")
    elif message.content_type == "audio":
        bot.reply_to(message, f"Аудио {message.audio.file_id} добавлено успешно!")


# Ошибка при работе бота
@bot.message_handler(commands=["error"])
def handle_error(message: types.Message):
    try:
        raise ValueError("Пример ошибки")
    except ValueError as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


# Ошибка при работе конвертации валют
@bot.message_handler(commands=["error_rate"])
def handle_error_rate(message: types.Message):
    try:
        exchange_rate = get_exchange_rate(
            "Неверный ключ",
            "USD",
            "EUR"
        )
    except ValueError as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


# Конвертация валют при inline-запросе
@bot.inline_handler(func=lambda query: True)
def inline_query_conversion(query: types.InlineQuery):
    try:
        input_text = query.query.strip()
        if input_text.lower() == "exchange":
            # Логика обработки конвертации валют
            # Например, можно предложить пользователю выбрать валюту через инлайн-клавиатуру
            markup = types.InlineKeyboardMarkup()
            # Добавляем кнопки для популярных валют
            for cur in ["USD", "EUR", "TRY", "BYN", "RUB", "PLN"]:
                markup.add(types.InlineKeyboardButton(text=cur, callback_data=f"from:{cur}"))
            bot.answer_inline_query(query.id, [types.InlineQueryResultArticle(
                id="choose_currency",
                title="Выберите валюту",
                input_message_content=types.InputTextMessageContent(
                    message_text="Выберите валюту из предложенного списка."),
                reply_markup=markup
            )])

    except Exception as e:
        bot.answer_inline_query(query.id, results=[])
#---------------------------------------------------------------------
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
    bot.send_document(
        chat_id=message.chat.id,
        document=file_text_doc,
        visible_file_name="yor_file_from_pc.txt"
    )

#Реакция на событие - по опорному слову выдаётся актуальная погода в городе Минск
@bot.message_handler(text_contains='погода')
def handle_weather_request(message: types.Message):
    weather_info = get_weather("Минск", config.OPENWEATHER_API_KEY)
    bot.send_message(message.chat.id, text=weather_info)

# Команды менюшки_11
# Отправка пользователю актуальной погоды в городе Минск
@bot.message_handler(commands=["weather"])
def command_weather_request(message: types.Message):
    weather_info = get_weather("Минск", config.OPENWEATHER_API_KEY)
    bot.send_message(message.chat.id, text=weather_info)

# Команды менюшки_12
# Отправка пользователю id чата
@bot.message_handler(commands=["chat_id"])
def handle_chat_id_request(message: types.Message):
    text = f'Айди чата: {message.chat.id}'
    bot.send_message(message.chat.id,text=text)

# Команды менюшки_13(скрытая)(1)
# Отправка пользователю id чата
@bot.message_handler(commands=["admin"], is_bot_admin=True)
def handle_admin_secret(message: types.Message):
    bot.send_message(message.chat.id, text=messagepy.ADMIN)
# Команды менюшки_13(скрытая)(2)
# Отправка пользователю id чата
@bot.message_handler(commands=["admin"], is_bot_admin=False)
def handle_not_admin_secret(message: types.Message):
    bot.send_message(message.chat.id, text=messagepy.NOT_ADMIN)

# Команды менюшки_14
# Изменяет шрифт текста
@bot.message_handler(commands=["md"])
def send_markdown_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messagepy.markdown_text,
        parse_mode="MarkdownV2"
    )

# Команды менюшки_15
# Конвертация валют
@bot.message_handler(commands=["usd_to_bel_rub"])
def convert_usd_to_bel_rub(message: types.Message):
    arguments = util.extract_arguments(message.text)
    if not arguments:
        bot.send_message(
            chat_id=message.chat.id,
            text=messagepy.convert_usd_to_bel_rub_how_to,
            parse_mode="HTML"
        )
        return

    try:
        usd_amount = float(arguments)
    except ValueError:
        text = formatting.format_text(
            formatting.format_text(messagepy.invalid_argument_text, formatting.hcode(arguments), separator=""),
            messagepy.convert_usd_to_bel_rub_how_to)
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML"
        )
        return

    try:
        exchange_rate = get_exchange_rate(config.EXCHANGERATE_API_KEY, "USD", "BYN")
        bel_rub_amount = usd_amount * exchange_rate
        bot.send_message(
            chat_id=message.chat.id,
            text=messagepy.format_usd_to_bel_rub_message(
                usd_amount=usd_amount,
                bel_rub_amount=bel_rub_amount
            ),
            parse_mode="HTML")
    except ValueError as e:
        bot.send_message(
            chat_id=message.chat.id,
            text=str(e),
            parse_mode="HTML"
        )

# Команды менюшки_16
# Обработчик команды set_my_currency, чтобы пользователь мог добавить свою валюту
@bot.message_handler(commands=["set_my_currency"])
def handle_set_my_currency(message: types.Message):
    msg = bot.send_message(message.chat.id, "Введите код валюты, которую вы хотите добавить (например, USD, EUR):")
    bot.register_next_step_handler(msg, process_set_my_currency)

def process_set_my_currency(message: types.Message):
    currency_code = message.text.strip().upper()
    if currency_code_pattern.match(currency_code):
        user_id = str(message.from_user.id)
        if user_id not in user_currencies:
            user_currencies[user_id] = []
        if currency_code not in user_currencies[user_id]:
            user_currencies[user_id].append(currency_code)
            save_user_currencies(user_currencies)
            bot.send_message(message.chat.id, f"Валюта {currency_code} успешно добавлена!")
        else:
            bot.send_message(message.chat.id, f"Валюта {currency_code} уже добавлена.")
    else:
        bot.send_message(message.chat.id, "Неверный код валюты. Пожалуйста, введите трехбуквенный код валюты.")

# Обработка команды delete_my_currency
@bot.message_handler(commands=["delete_my_currency"])
def handle_delete_my_currency(message: types.Message):
    msg = bot.send_message(message.chat.id, "Введите код валюты, которую вы хотите удалить (например, USD, EUR):")
    bot.register_next_step_handler(msg, process_delete_my_currency)

def process_delete_my_currency(message: types.Message):
    currency_code = message.text.strip().upper()
    user_id = str(message.from_user.id)
    if currency_code in user_currencies.get(user_id, []):
        user_currencies[user_id].remove(currency_code)
        save_user_currencies(user_currencies)
        bot.send_message(message.chat.id, f"Валюта {currency_code} успешно удалена!")
    else:
        bot.send_message(message.chat.id, f"Валюта {currency_code} не найдена в вашем списке.")

#----------------------------------------------------------------------------


#Реакция на событие - отправка стикера
@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=formatting.mbold("Классный стикер!"),
        parse_mode="MarkdownV2",
        reply_to_message_id=message.id
    )


#Реакция на событие - реакция на подпись под картинкой "волк" (1)
def is_wolf_in_caption(message: types.Message):
    return message.caption and "волк" in message.caption.lower()

#Реакция на событие - реакция на подпись под картинкой "волк" (2)
@bot.message_handler(content_types=["photo"], func=is_wolf_in_caption)
def handle_photo_with_wolf_caption(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Nice photo!',
        reply_to_message_id=message.id
    )

# Реакция на событие - дублируем последнее фото без подписи
@bot.message_handler(content_types=["photo"])
def handle_photo(message: types.Message):
    photo_file_id = message.photo[-1].file_id
    caption_text = 'Классное фото!'
    if message.caption:
        caption_text += "\nПодпись:\n" + message.caption
    bot.send_photo(
        message.chat.id,
        photo=photo_file_id,
        reply_to_message_id=message.id,
        caption=caption_text
    )

# Реакция на событие - голосовое сообщение
@bot.message_handler(content_types=["voice"])
def handle_voice(message: types.Message):
    bot.send_message(
        message.chat.id,
        "К сожалению я не могу прослушать что вы сказали :(",
        reply_to_message_id=message.id
    )

# Копирование и отсылка сообщения в том же формате,
# в котором нам его отправил пользователь
@bot.message_handler()
def copy_incoming_message(message: types.Message):
    # if message.entities:
    #     print('message entities:')
    #     for entity in message.entities:
    #         print(entity)
    bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.id
    )

# Реакция на событие - ответ если определенные слова есть в сообщении пользователя
@bot.message_handler()
def send_echo_message(message: types.Message):
    text = message.text
    # if 'привет' in text.lower():
    #     text = 'Привет! Как ты?'
    # elif 'как дела' in text.lower():
    #     text = 'Нормально!'
    # elif 'пока' in text.lower() or 'до свидания' in text.lower():
    #     text = 'До новых встреч!'
    # elif 'Милан' in text.lower():
    #     text = 'Создатель'
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        entities=message.entities
    )



#Проверка, для запуска именно этого файла
if __name__ == "__main__":
    bot.enable_saving_states()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True)




