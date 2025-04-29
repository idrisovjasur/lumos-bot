from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.inline.text import (appeal_ru, appeal_uz, complaint_ru,
                                   complaint_uz, offer_ru, offer_uz, question_uz, question_ru, back_uz, back_ru)
from loader import db
from states.main_states import AppealStates
from keyboards.inline.registration import edit_language, main_keyboard, appeal_keyboard
from filters.language import get_language
from handlers.users.text import answer_function, offer_text_ru
from handlers.users import text
from aiogram.filters import StateFilter


main_router = Router()

@main_router.message(F.text.in_([text.profile_ru_text, text.profile_uz_text]))
async def profile_function(message: Message):
    data = await answer_function(message)
    answer = data[0]
    language = data[1]
    await message.answer(answer, reply_markup=await edit_language(language))


@main_router.callback_query(F.data == text.edit_text_data)
async def edit_user_languages(callback_query: CallbackQuery, state: FSMContext):
    language = await get_language(callback_query.from_user.id)
    if language == 'ru':
        await db.update_user_language('uz', callback_query.from_user.id)
        await callback_query.answer(text.update_text_uz, show_alert=True)
        await callback_query.message.delete()
        await callback_query.message.answer(text.menu_uz, reply_markup= await main_keyboard('uz'))
    elif language == 'uz':
        await db.update_user_language(language='ru', telegram_id=callback_query.from_user.id)
        await callback_query.answer(text.update_text_ru, show_alert=True)
        await callback_query.message.delete()
        await callback_query.message.answer(text.menu_ru, reply_markup= await main_keyboard('ru'))


@main_router.message(F.text.in_([appeal_ru, appeal_uz]))
async def appeal_function(message: Message):
    lang = await get_language(message.from_user.id)
    await message.answer(text = 'appeal', reply_markup= await appeal_keyboard(lang))


@main_router.message(F.text.in_([complaint_ru,
                                 complaint_uz, offer_ru, offer_uz, question_uz, question_ru]))
async def main_appeal_function(message: Message, state: FSMContext):
    if message.text == complaint_ru:
        await message.answer(text = text.complaint_text_ru)
        await state.update_data(type = complaint_ru)
        await state.set_state(AppealStates.appeal)
    elif message.text == complaint_uz:
        await message.answer(text=text.complaint_text_uz)
        await state.update_data(type = complaint_uz)
        await state.set_state(AppealStates.appeal)
    elif message.text == offer_ru:
        await message.answer(text=offer_text_ru)
        await state.update_data(type = offer_ru)
        await state.set_state(AppealStates.appeal)
    elif message.text == offer_uz:
        await message.answer(text=text.offer_text_uz)
        await state.update_data(type=offer_uz)
        await state.set_state(AppealStates.appeal)
    elif message.text == question_uz:
        await message.answer(text=text.question_text_uz)
        await state.update_data(type=question_uz)
        await state.set_state(AppealStates.appeal)
    elif message.text == question_ru:
        await message.answer(text=text.question_text_ru)
        await state.update_data(type=question_ru)
        await state.set_state(AppealStates.appeal)

@main_router.message(StateFilter('*'), F.text.in_([back_uz, back_ru]))
async def back_appeal(message: Message):
    lang = await get_language(message.from_user.id)
    if lang == 'ru':
        await message.answer(text = text.menu_ru, reply_markup= await main_keyboard('ru'))
    else:
        await message.answer(text = text.menu_uz, reply_markup= await main_keyboard('uz'))

@main_router.message(AppealStates.appeal)
async def appeal_text_save(message: Message, state: FSMContext):
    user = await db.select_user(telegram_id=message.from_user.id)
    data = await state.get_data()
    question_type = data.get('type')
    name = user.get('name')
    surname = user.get('surname')
    phone = user.get('phone')
    class_name = user.get('class_name')
    lang = user.get('language')
    text_appeal = message.text
    try:
        await db.add_appeal(name, surname, phone, class_name, text_appeal, question_type)
        if lang == 'ru':
            await message.answer(text=text.finish_appeal_ru, reply_markup= await main_keyboard('ru'))
        else:
            await message.answer(text=text.finish_appeal_uz, reply_markup= await main_keyboard('uz'))
        await state.clear()
    except Exception as e:
        print(e)



