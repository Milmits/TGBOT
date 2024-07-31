UNKNOWN_JOKES = [
    ("Завтра буду спать до 12 дня.\n(Запись понравилась 15 газонокосильщикам)"),
    'Выспался? Уже неплохо. Не надо ждать от жизни многого.',
    'Легче всего встается по будильнику в день зарплаты.',
    'Не будет шутки, я устал!!!'
]

help_message = """Привет, Доступные команды:
    /start - начало работы с ботом
    /help - помощь (это сообщение)
    /joke - случайная шутка xD
    и много чего еще...

Этот бот отправит вам то же сообщение, что и вы ему!
"""
start_message = 'Привет, давай знакомиться!!'

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