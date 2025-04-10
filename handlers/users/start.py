from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.inline.registration import register_key, main_keyboard
import json
from loader import db

start_router = Router()


@start_router.message(CommandStart())
async def start_function(message: Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    if not user:
        await message.answer(
            text = 'Please Registration',
            reply_markup = register_key,
        )
    else:
        await message.answer(text = 'Main', reply_markup=main_keyboard)


@start_router.message(F.web_app_data)
async def register_function(message: Message):
    data = json.loads(message.web_app_data.data)
    name = data.get("name")
    surname = data.get("surname")
    phone = data.get("phone")
    class_name = data.get("className")
    try:
        await db.add_user(name = name, surname = surname, phone = phone, class_name=class_name,
                          username=message.from_user.username, telegram_id=message.from_user.id)
    except Exception as e:
        print(e)
    await message.answer("Thank you for registering!", reply_markup=main_keyboard)


