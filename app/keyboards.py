from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

# запуск заполнения формы бота
main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Начать')
    ]
    ],
                resize_keyboard=True,
                input_field_placeholder="Начните!"
)

# Товарищский ли матч 'yes' 'no'
isComrade = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='yes'),
        InlineKeyboardButton(text='Нет', callback_data='no')
    ]
])

# согласие или нет на ввод состава команд 'yes_s' 'no_s'
isCheck = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да введу', callback_data='yes_s'),
        InlineKeyboardButton(text='Нет не буду', callback_data='no_s')
    ]
])

#   проверка формы 'check_form'
checkForm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отправить", callback_data='check_form')
    ]
])

#   Отправка формы "request_form"
buttonDone = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отправить", callback_data="request_form")
    ]
])



