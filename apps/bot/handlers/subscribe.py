from aiogram.types import Message
from asgiref.sync import sync_to_async
from apps.subscriptions.models import Tariff, Subscription
from apps.bot.keyboards import tariff_menu
from django.db import close_old_connections
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@sync_to_async
def get_active_tariffs():
    close_old_connections()
    tariffs = Tariff.objects.filter(is_active=True)
    # Tariff obyektlarini dict sifatida qaytarish
    return [
        {
            'id': t.id,
            'name': t.name,
            'price': t.price,
            'duration_days': t.duration_days,
            'description': t.description
        }
        for t in tariffs
    ]

@sync_to_async
def check_active_subscription(telegram_id):
    """Foydalanuvchining aktiv obunasini tekshirish"""
    close_old_connections()
    from apps.users.models import User
    
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None
    
    subscription = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gte=timezone.now()
    ).first()
    
    if subscription:
        return {
            'tariff_name': subscription.tariff.name,
            'end_date': subscription.end_date
        }
    return None

async def cmd_subscribe(message: Message):
    logger.info(f"Subscribe handler called by {message.from_user.id}")
    
    # Avval aktiv obuna borligini tekshirish
    active_subscription = await check_active_subscription(message.from_user.id)
    
    if active_subscription:
        text = (
            f"✅ Sizda aktiv obuna mavjud!\n\n"
            f"📦 Tarif: {active_subscription['tariff_name']}\n"
            f"📅 Amal qilish muddati: {active_subscription['end_date'].strftime('%d.%m.%Y')}\n\n"
            "Tarifni almashtirmoqchimisiz? Quyidagi tariflardan birini tanlang:"
        )
    else:
        text = "💳 Obuna tariflari:\n\n"
    
    tariffs = await get_active_tariffs()
    
    if not tariffs:
        await message.answer("❌ Hozirda mavjud tariflar yo'q.")
        return
    
    if not active_subscription:
        for tariff in tariffs:
            text += f"📦 {tariff['name']}\n"
            text += f"💰 Narx: {tariff['price']} so'm\n"
            text += f"📅 Muddat: {tariff['duration_days']} kun\n"
            text += f"📝 {tariff['description']}\n\n"
    
    await message.answer(text, reply_markup=tariff_menu(tariffs))
    logger.info(f"Subscribe message sent to {message.from_user.id}")
