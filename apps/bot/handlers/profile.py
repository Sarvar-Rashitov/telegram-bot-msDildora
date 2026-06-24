from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.users.models import User
from apps.subscriptions.models import Subscription

@sync_to_async
def get_user_profile(telegram_id):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None, None
    
    active_subscription = Subscription.objects.filter(
        user=user, 
        status='active'
    ).first()
    
    return user, active_subscription

async def cmd_profile(message: Message):
    user, active_subscription = await get_user_profile(message.from_user.id)
    
    if not user:
        await message.answer("❌ Profil topilmadi. /start bosing.")
        return
    
    text = f"👤 Profil\n\n"
    text += f"📱 Telegram ID: {user.telegram_id}\n"
    text += f"💰 Balans: {user.balance} so'm\n"
    text += f"🔗 Referal kod: {user.referral_code}\n\n"
    
    if active_subscription:
        text += f"✅ Aktiv obuna: {active_subscription.tariff.name}\n"
        text += f"📅 Amal qilish muddati: {active_subscription.end_date.strftime('%d.%m.%Y')}"
    else:
        text += "❌ Faol obuna yo'q"
    
    await message.answer(text)
