from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Чат')
    ]
    ],
                resize_keyboard=True,
                input_field_placeholder="Выберите пункт меню"
)