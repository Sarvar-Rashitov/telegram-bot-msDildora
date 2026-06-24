from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async
from apps.subscriptions.models import Tariff, Subscription
from apps.users.models import User
from apps.payments.utils import create_payment
from apps.bot.keyboards import payment_menu

@sync_to_async
def create_subscription_and_payment(telegram_id, tariff_id):
    try:
        tariff = Tariff.objects.get(id=tariff_id, is_active=True)
        user = User.objects.get(telegram_id=telegram_id)
        
        subscription = Subscription.objects.create(
            user=user,
            tariff=tariff,
            status='pending'
        )
        
        payment = create_payment(user, subscription, tariff.price)
        
        return {
            'success': True,
            'tariff_name': tariff.name,
            'tariff_price': str(tariff.price),
            'tariff_duration': tariff.duration_days,
            'payment_url': payment.payment_url
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

async def handle_tariff_callback(callback: CallbackQuery):
    """Handle tariff selection"""
    tariff_id = int(callback.data.split('_')[1])
    
    result = await create_subscription_and_payment(callback.from_user.id, tariff_id)
    
    if result['success']:
        text = (
            f"💳 Obuna: {result['tariff_name']}\n"
            f"💰 Narx: {result['tariff_price']} so'm\n"
            f"📅 Muddat: {result['tariff_duration']} kun\n\n"
            "To'lov tugmasini bosing va to'lovni amalga oshiring.\n"
            "To'lovdan keyin 'To'lovni tasdiqlash' tugmasini bosing."
        )
        
        await callback.message.answer(
            text,
            reply_markup=payment_menu(result['payment_url'])
        )
        await callback.answer()
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@sync_to_async
def check_user_payment(telegram_id):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        subscription = Subscription.objects.filter(
            user=user,
            status='pending'
        ).order_by('-created_at').first()
        
        if not subscription:
            return {'found': False}
        
        payment = subscription.payments.filter(status='success').first()
        
        return {
            'found': True,
            'paid': payment is not None
        }
    except:
        return {'found': False}

async def handle_check_payment(callback: CallbackQuery):
    """Check payment status"""
    result = await check_user_payment(callback.from_user.id)
    
    if not result['found']:
        await callback.answer("❌ Obuna topilmadi", show_alert=True)
        return
    
    if result['paid']:
        await callback.message.answer(
            "✅ To'lov muvaffaqiyatli amalga oshirildi!\n"
            "Kanalga kirish uchun quyidagi havola orqali kiring."
        )
    else:
        await callback.answer(
            "⏳ To'lov hali tasdiqlanmagan. Iltimos, biroz kuting.",
            show_alert=True
        )
