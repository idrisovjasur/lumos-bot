from loader import db

async def get_language(user_id):
    user = await db.select_user(
        telegram_id=user_id,
    )
    return user['language']
