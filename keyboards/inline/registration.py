from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

register_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Registration",
                web_app=WebAppInfo(url="https://katyolusta.uz/webapp/")
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Appeal'), KeyboardButton(text = 'Profile'),
        ],
    ],resize_keyboard=True
)



