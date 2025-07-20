from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Начать')
    ]
    ],
                resize_keyboard=True,
                input_field_placeholder="Введите дату события"
)

isComrade = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='yes'),
        InlineKeyboardButton(text='Нет', callback_data='no')
    ]
])

buttonDone = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Отправить', callback_data="request_form")
    ]
])

checkForm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Проверить", callback_data='check_form')
    ]
])