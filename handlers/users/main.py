from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loader import db
from states.main_states import MainStates

main_router = Router()


@main_router.message(F.text=='Profile')
async def profile_function(message: Message):
    user = await db.select_user(telegram_id = message.from_user.id)
    name = user.get('name')
    surname = user.get('surname')
    phone = user.get('phone')
    class_name = user.get('class_name')
    answer = f"<b>Name: {name}\nSurname: {surname}\nPhone: {phone}\nClassName: {class_name}</b>"
    await message.answer(answer)

@main_router.message(F.text=='Appeal')
async def appeal_function(message: Message, state: FSMContext):
    await state.set_state(MainStates.appeal)
    await message.answer(text = 'Write your request and proposal...')

@main_router.message(MainStates.appeal)
async def appeal_re_function(message: Message, state: FSMContext):
    await state.update_data(text = message.text)
    data = await state.get_data()
    user = await db.select_user(telegram_id = message.from_user.id)
    text = data.get('text')
    name = user.get('name')
    surname = user.get('surname')
    phone = user.get('phone')
    class_name = user.get('class_name')
    try:
        await db.add_appeal(name, surname, phone, class_name, text)
        await message.answer(text = 'Your appeal has been added. Thank you!')
        await state.clear()
    except Exception as e:
        print(e)


