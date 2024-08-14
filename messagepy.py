from telebot import formatting, types
from telebot import types


UNKNOWN_JOKES = [
    ("Завтра буду спать до 12 дня.\n(Запись понравилась 15 газонокосильщикам)"),
    'Выспался? Уже неплохо. Не надо ждать от жизни многого.',
    'Легче всего встается по будильнику в день зарплаты.',
    'Не будет шутки, я устал!!!'
]

help_message = """Привет, Доступные команды:
    
    @MilanBirthdayBot 35 - Конвертор валют
    /start - начало работы с ботом
    /help - помощь (это сообщение)
    /joke - случайная шутка xD
    и много чего еще...
    /usd_to_bel_rub - конвертировать 1 доллар в белорусские рубли
    /cvt 1 currancy - конвертировать 1 валюту в белорусские рубли

Этот бот отправит вам то же сообщение, что и вы ему!
"""
start_message = 'Привет, давай знакомиться!!'

convert_usd_to_bel_rub_how_to = formatting.format_text('Пожалуйста укажите аргумент для конвертации:',
                                                       formatting.hcode("/usd_to_bel_rub 1"))

cvt_help_message = formatting.format_text('Пожалуйста укажите аргумент для конвертации:',
                                                       formatting.hcode("/usd_to_bel_rub 1"))

cvt_how_to = formatting.format_text(formatting.hcode("/usd_to_bel_rub 1"))

invalid_argument_text = "Неправильный аргумент: "

from telebot import types


def format_conversion_result(amount, from_currency, to_currency, converted_amount):
    return (
        f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
    )


def create_inline_query_result(amount, from_currency, to_currency, converted_amount):
    result_text = format_conversion_result(amount, from_currency, to_currency, converted_amount)

    return types.InlineQueryResultArticle(
        id=to_currency,
        title=f"{amount} {from_currency} в {to_currency}",
        input_message_content=types.InputTextMessageContent(
            message_text=result_text,
            parse_mode="HTML"
        ),
        description=result_text
    )

def format_usd_to_bel_rub_message(usd_amount, bel_rub_amount):
    return formatting.format_text(formatting.hcode(f"{usd_amount:,.2f}"), "USD это примерно", formatting.hcode(f"{bel_rub_amount:,.2f}"), "BEL RUB ", separator=" ")

ADMIN = 'Безумно рад вашему возвращению Overlord!!!!!!'
NOT_ADMIN = 'Извините, но у вы не имеете статуса ADMIN'

markdown_text = """
*bold \*text*
_italic \_text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=625670582)
![👍](tg://emoji?id=5368324170671202286)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
#pre-formatted fixed-width code block written in the Python programming language

@bot.message_handler(commands=["md"])
def send_markdown_message(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=messagepy.markdown_text, parse_mode="MarkdownV2")

```
>Block quotation started
>Block quotation continued
>Block quotation continued
>Block quotation continued
>The last line of the block quotation
**>The expandable block quotation started right after the previous block quotation
>It is separated from the previous block quotation by an empty bold entity
>Expandable block quotation continued
>Hidden by default part of the expandable block quotation started
>Expandable block quotation continued
>The last line of the expandable block quotation with the expandability mark||
"""


#Опросник
opros_cancel_suggestion = formatting.format_text(
    "",
    formatting.format_text(
        "Отменить опрос можно командой /cancel или просто отправьте",
        formatting.hcode("отмена"),
        separator=" ",
    )
)

opros_message_welcome_what_is_full_name = formatting.format_text(
    "Пожалуйтса представьтесь",
    "Напишите ваше полное имя: Например - Иван Иванов",
    opros_cancel_suggestion,
)

opros_message_full_name_not_text = formatting.format_text(
    "Это не текст, мы бы хотели узнать ваше имя",
    "Пожалуйста укажите ваше настоящее имя",
    opros_cancel_suggestion,
)

opros_message_full_name_ok_and_ask_for_email = formatting.format_text(
    "Добро пожаловать, {full_name}!",
    "Пожалуйста отправьте ваш email, ",
)

opros_message_email_not_ok = formatting.format_text(
    "Это не настоящий email",
    "Пожалуйста укажите валидный",
    opros_cancel_suggestion,

)

opros_message_email_is_ok = formatting.format_text(
    "Почту записали, можно подписать вас на рассылку?",
)

opros_message_invalid_yes_or_no = formatting.format_text(
    "Не понимаю, пожалуйста укажите да или нет",
)

opros_message_cancelled = formatting.format_text(
    "Опрос отменен. Пройти заново: /opros",
)

random_message_text = formatting.format_text(
    "Вот сообщение с клавиатурой с рандомом",
)

#00000000000000000000000000000000000000000000000000000000000000
random_message_text = "Вот сообщение с клавиатурой с рандомом"

# Обновляем help-сообщение
help_message_text = (
    "Доступные команды:\n"
    "/start - Запуск бота\n"
    "/dev_opros - Пройти опрос для программистов\n"
    "/cancel - Отменить текущий опрос"
)
