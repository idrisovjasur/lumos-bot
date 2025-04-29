from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from keyboards.inline import text

register_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Registration",
                web_app=WebAppInfo(url="https://katyolusta.uz")
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


async def main_keyboard(language):
    keyboard = ReplyKeyboardBuilder()
    if language == 'ru':
        keyboard.add(KeyboardButton(text=text.appeal_ru))
        keyboard.add(KeyboardButton(text=text.profile_ru))
        keyboard.add(KeyboardButton(text=text.event_ru))
        keyboard.add(KeyboardButton(text=text.organizational_ru))
    elif language == 'uz':
        keyboard.add(KeyboardButton(text=text.appeal_uz))
        keyboard.add(KeyboardButton(text=text.profile_uz))
        keyboard.add(KeyboardButton(text=text.event_uz))
        keyboard.add(KeyboardButton(text=text.organizational_uz))

    return keyboard.adjust(2).as_markup(resize_keyboard=True)

async def edit_language(lang):
    keyboard = InlineKeyboardBuilder()
    if lang == 'ru':
        keyboard.add(InlineKeyboardButton(text=text.edit_lang_ru, callback_data='edit_lang'))
    elif lang == 'uz':
        keyboard.add(InlineKeyboardButton(text=text.edit_lang_uz, callback_data='edit_lang'))

    return keyboard.as_markup()


async def appeal_keyboard(language):
    keyboard = ReplyKeyboardBuilder()
    if language == 'uz':
        keyboard.add(KeyboardButton(text=text.question_uz))
        keyboard.add(KeyboardButton(text=text.offer_uz))
        keyboard.add(KeyboardButton(text=text.complaint_uz))
        keyboard.add(KeyboardButton(text=text.back_uz))
    elif language == 'ru':
        keyboard.add(KeyboardButton(text=text.question_ru))
        keyboard.add(KeyboardButton(text=text.offer_ru))
        keyboard.add(KeyboardButton(text=text.complaint_ru))
        keyboard.add(KeyboardButton(text=text.back_ru))

    return keyboard.adjust(2).as_markup(resize_keyboard=True)