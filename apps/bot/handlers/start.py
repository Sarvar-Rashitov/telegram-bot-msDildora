from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.bot.keyboards import main_menu
from apps.users.models import User
from django.db import close_old_connections
import random
import string

@sync_to_async
def get_or_create_user(telegram_id, username, first_name, last_name):
    close_old_connections()
    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': username or f"user_{telegram_id}",
            'telegram_username': username,
            'first_name': first_name or '',
            'last_name': last_name or '',
            'referral_code': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
    )
    return user, created

async def cmd_start(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or ''
    last_name = message.from_user.last_name or ''
    
    user, created = await get_or_create_user(telegram_id, username, first_name, last_name)
    
    if created:
        welcome_text = (
            f"👋 Xush kelibsiz, {first_name}!\n\n"
            "Bu bot orqali premium kanalimizga obuna bo'lishingiz mumkin.\n\n"
            "📝 To'liq imkoniyatlardan foydalanish uchun ro'yxatdan o'ting!"
        )
    else:
        welcome_text = (
            f"👋 Qaytganingizdan xursandmiz, {first_name}!\n\n"
            "Quyidagi tugmalardan birini tanlang:"
        )
    
    await message.answer(welcome_text, reply_markup=main_menu(user.is_registered))
