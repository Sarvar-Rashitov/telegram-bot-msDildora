from aiogram.types import Message, ChatMemberUpdated
from aiogram import Bot
from asgiref.sync import sync_to_async
from apps.users.models import User
from apps.subscriptions.models import Subscription
from apps.channels.models import TelegramChannel
from apps.bot.keyboards import channel_invite_keyboard
from django.db import close_old_connections
from django.utils import timezone

@sync_to_async
def get_user_active_subscription(telegram_id):
    """Foydalanuvchining aktiv obunasini tekshirish"""
    close_old_connections()
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None, None
    
    subscription = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gte=timezone.now()
    ).first()
    
    return user, subscription

@sync_to_async
def get_primary_channel():
    """Asosiy private kanalni olish"""
    close_old_connections()
    channel = TelegramChannel.objects.filter(is_active=True).first()
    return channel

async def cmd_join_channel(message: Message):
    """Kanalga o'tish handler"""
    user, subscription = await get_user_active_subscription(message.from_user.id)
    
    if not user:
        await message.answer("❌ Profil topilmadi. /start bosing.")
        return
    
    if not subscription:
        await message.answer(
            "❌ Sizda aktiv obuna yo'q!\n\n"
            "📢 Kanalga kirish uchun avval obuna sotib oling.\n\n"
            "💳 'Obuna bo'lish' tugmasini bosing va tarifni tanlang."
        )
        return
    
    channel = await get_primary_channel()
    
    if not channel or not channel.invite_link:
        await message.answer(
            "❌ Kanal havolasi topilmadi.\n"
            "Iltimos, admin bilan bog'laning."
        )
        return
    
    # Obuna bor bo'lsa, bevosita kanalga o'tish
    await message.answer(
        f"✅ Sizda aktiv obuna bor!\n\n"
        f"📢 Kanal: {channel.name}\n"
        f"📅 Obuna amal qilish muddati: {subscription.end_date.strftime('%d.%m.%Y')}\n\n"
        "Quyidagi tugma orqali kanalga o'ting:",
        reply_markup=channel_invite_keyboard(channel.invite_link)
    )

async def check_chat_member(chat_member: ChatMemberUpdated, bot: Bot):
    """
    Kanalga kirayotgan odamni obuna tekshirish.
    Agar obuna bo'lmasa, kanaldan chiqarish.
    """
    # Faqat channel join event'larini qayta ishlaymiz
    if chat_member.new_chat_member.status not in ['member', 'administrator', 'creator']:
        return
    
    telegram_id = chat_member.from_user.id
    channel_id = chat_member.chat.id
    
    user, subscription = await get_user_active_subscription(telegram_id)
    
    # Agar aktiv obuna bo'lmasa, kanaldan chiqarish
    if not subscription:
        try:
            await bot.ban_chat_member(
                chat_id=channel_id,
                user_id=telegram_id
            )
            # Ban'ni darhol olib tashlash (faqat kick qilish)
            await bot.unban_chat_member(
                chat_id=channel_id,
                user_id=telegram_id,
                only_if_banned=True
            )
            
            # Foydalanuvchiga xabar yuborish
            try:
                await bot.send_message(
                    telegram_id,
                    "❌ Sizda aktiv obuna yo'q!\n\n"
                    "Kanalga kirish uchun obuna sotib oling.\n"
                    "💳 Obuna bo'lish tugmasini bosing."
                )
            except:
                pass
        except Exception as e:
            print(f"Kanaldan chiqarish xatosi: {e}")
