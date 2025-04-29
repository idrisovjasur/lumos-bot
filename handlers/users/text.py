from loader import db
async def answer_function(message):
    user = await db.select_user(telegram_id=message.from_user.id)
    name = user.get('name')
    surname = user.get('surname')
    phone = user.get('phone')
    class_name = user.get('class_name')
    language = user.get('language')
    if language == 'ru':
        answer = (
            "<b>👤 Профиль пользователя</b>\n\n"
            f"🔹 <b>Имя:</b> {name}\n"
            f"🔹 <b>Фамилия:</b> {surname}\n"
            f"📞 <b>Телефон:</b> {phone}\n"
            f"🏫 <b>Класс:</b> {class_name}\n"
            f"🌐 <b>Язык:</b> Русский"
        )
        return  [answer, language]

    elif language == 'uz':
        answer = (
            "<b>👤 Foydalanuvchi profili</b>\n\n"
            f"🔹 <b>Ism:</b> {name}\n"
            f"🔹 <b>Familiya:</b> {surname}\n"
            f"📞 <b>Telefon:</b> {phone}\n"
            f"🏫 <b>Sinf:</b> {class_name}\n"
            f"🌐 <b>Til:</b> O‘zbekcha"
        )

        return [answer, language]


update_text_ru = '✅ Язык успешно изменен!'
update_text_uz = '✅ Til muvoffaqqiyatli o\'zgartirilldi!'
profile_ru_text = '👤 Мой профиль'
profile_uz_text = '👤 Profilim'
edit_text_data = 'edit_lang'
menu_uz = 'Menyu'
menu_ru = 'Меню'
register_ru = "Спасибо за регистрацию!"
register_uz = "Roʻyxatdan oʻtganingiz uchun tashakkur!"
start_text = ('Пожалуйста, зарегистрируйтесь\n\n'
              'Ro\'yxatdan o\'tish')
complaint_text_ru = 'Напишите свою жалобу.'
complaint_text_uz = 'Shikoyatingizni yozib qoldiring.'
offer_text_uz = 'Taklifingizni yozib qoldiring.'
offer_text_ru = 'Запишите свое предложение.'
question_text_uz = 'Savolingzni yozib qoldiring.'
question_text_ru = 'Запишите свой вопрос.'
finish_appeal_ru = 'Ваша апелляция добавлена. Спасибо!'
finish_appeal_uz = 'Murojaatingiz qabul qilindi. Rahmat!'
appeal_type_ru = 'Выберите тип приложения'
appeal_type_uz = 'Murojaat turini tanlang'