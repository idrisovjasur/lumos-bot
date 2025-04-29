from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from filters.language import get_language
from handlers.users import text
from keyboards.inline.registration import register_key, main_keyboard
import json
from loader import db

start_router = Router()

@start_router.message(CommandStart())
async def start_function(message: Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    if not user:
        await message.answer(
            text = text.start_text,
            reply_markup = register_key,
        )
    else:
        lang = await get_language(message.from_user.id)
        if lang == 'ru':
            await message.answer(text = text.menu_ru, reply_markup= await main_keyboard(lang))
        elif lang == 'uz':
            await message.answer(text = text.menu_uz, reply_markup= await main_keyboard(lang))


@start_router.message(F.web_app_data)
async def register_function(message: Message):
    data = json.loads(message.web_app_data.data)
    name = data.get("name")
    surname = data.get("surname")
    phone = data.get("phone")
    class_name = data.get("className")
    language = data.get("lang")
    try:
        await db.add_user(name = name, surname = surname, phone = phone, class_name=class_name,
                          username=message.from_user.username, telegram_id=message.from_user.id, language=language)
    except Exception as e:
        print(e)
    if language == 'ru':
        await message.answer(text.register_ru, reply_markup=await main_keyboard(language))
    elif language == 'uz':
        await message.answer(text.register_uz, reply_markup=await main_keyboard(language))


