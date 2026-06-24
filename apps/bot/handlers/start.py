from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.bot.keyboards import main_menu
from apps.users.models import User
import random
import string

@sync_to_async
def get_or_create_user(telegram_id, username):
    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': username,
            'referral_code': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    )
    return user, created

async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or f"user_{telegram_id}"
    
    user, created = await get_or_create_user(telegram_id, username)
    
    welcome_text = (
        f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
        "Bu bot orqali premium kanalimizga obuna bo'lishingiz mumkin.\n\n"
        "Quyidagi tugmalardan birini tanlang:"
    )
    
    await message.answer(welcome_text, reply_markup=main_menu())
