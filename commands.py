from telebot.types import BotCommand

default_commands = [
    BotCommand("start", "Начало работы"),
    BotCommand("help", 'Помощь'),
    BotCommand("cvt", 'Генерация_валюты'),
    BotCommand("joke", 'Случайная шутка'),
    BotCommand("wolf", 'Фото волка'),
    BotCommand("sunrise_file", 'Фото восхода солнца(1)'),
    BotCommand("sunrise_by_id", 'Фото восхода солнца(2)'),
    BotCommand("sunrise_doc", 'Фото восхода солнца как документ (с диска ПК)'),
    BotCommand("wolf_doc_id", 'Фото волка как документ (по идентификатору фотографии)'),
    BotCommand("file_txt", 'Получить файл text.txt из каталога'),
    BotCommand("text", 'Отправить текстовый документ из памяти ПК'),
    BotCommand("weather", 'Погода на сегодня'),
    BotCommand("chat_id", 'Вы можете узнать фактический идентификатор чата'),
    BotCommand("md", 'Пометить текст'),
    BotCommand("usd_to_bel_rub", 'Конвертировать USD в BEL_RUB'),
    BotCommand("set_my_currency", 'Добавить валюту в меню'),
    BotCommand("delete_my_currency", 'Удалить валюту в меню'),
    BotCommand("opros", 'Опросник'),
]
