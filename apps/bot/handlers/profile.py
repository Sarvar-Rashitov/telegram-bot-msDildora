from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.users.models import User
from apps.subscriptions.models import Subscription
from django.db import close_old_connections
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@sync_to_async
def get_user_profile(telegram_id):
    close_old_connections()
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None, None
    
    active_subscription = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gte=timezone.now()
    ).first()
    
    # User ma'lumotlarini dict sifatida
    user_data = {
        'telegram_id': user.telegram_id,
        'telegram_username': user.telegram_username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'age': user.age,
        'occupation': user.occupation,
        'is_registered': user.is_registered,
        'balance': user.balance,
        'referral_code': user.referral_code,
    }
    
    # Subscription ma'lumotlarini dict sifatida
    subscription_data = None
    if active_subscription:
        subscription_data = {
            'tariff_name': active_subscription.tariff.name,
            'tariff_price': active_subscription.tariff.price,
            'start_date': active_subscription.start_date,
            'end_date': active_subscription.end_date,
        }
    
    return user_data, subscription_data

async def cmd_profile(message: Message):
    logger.info(f"Profile handler called by {message.from_user.id}")
    
    user, active_subscription = await get_user_profile(message.from_user.id)
    
    if not user:
        await message.answer("❌ Profil topilmadi. /start bosing.")
        return
    
    text = f"👤 Profil\n\n"
    
    if user['is_registered']:
        text += f"📝 Ro'yxatdan o'tgan: ✅\n"
        text += f"👤 {user['first_name']} {user['last_name']}\n"
        text += f"📱 Telefon: {user['phone']}\n"
        text += f"🎂 Yosh: {user['age']}\n"
        text += f"💼 Kasb: {user['occupation']}\n"
    else:
        text += f"📝 Ro'yxatdan o'tgan: ❌\n"
        text += f"Telegram: @{user['telegram_username'] or 'mavjud emas'}\n"
    
    text += f"\n📱 Telegram ID: {user['telegram_id']}\n"
    text += f"💰 Balans: {user['balance']} so'm\n"
    text += f"🔗 Referal kod: {user['referral_code']}\n\n"
    
    if active_subscription:
        text += f"✅ Aktiv obuna: {active_subscription['tariff_name']}\n"
        text += f"💰 Narx: {active_subscription['tariff_price']} so'm\n"
        text += f"📅 Boshlangan: {active_subscription['start_date'].strftime('%d.%m.%Y') if active_subscription['start_date'] else 'N/A'}\n"
        text += f"📅 Tugaydi: {active_subscription['end_date'].strftime('%d.%m.%Y')}"
    else:
        text += "❌ Faol obuna yo'q"
    
    await message.answer(text)
    logger.info(f"Profile sent to {message.from_user.id}")
