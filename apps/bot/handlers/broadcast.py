from aiogram import Bot
from aiogram.types import FSInputFile
from asgiref.sync import sync_to_async
from apps.broadcasts.models import Broadcast
from apps.users.models import User
from django.db import close_old_connections
import asyncio

@sync_to_async
def get_pending_broadcast():
    """Yuborishga tayyor broadcast olish"""
    close_old_connections()
    broadcast = Broadcast.objects.filter(status='draft').first()
    if broadcast:
        broadcast.status = 'sending'
        broadcast.save()
    return broadcast

@sync_to_async
def get_target_users(broadcast):
    """Yuborish uchun foydalanuvchilar ro'yxati"""
    close_old_connections()
    if broadcast.target_all:
        users = User.objects.filter(is_blocked=False, telegram_id__isnull=False)
    else:
        # Faqat registered userlar
        users = User.objects.filter(is_blocked=False, is_registered=True, telegram_id__isnull=False)
    return list(users.values_list('telegram_id', flat=True))

@sync_to_async
def update_broadcast_stats(broadcast_id, sent_count, failed_count):
    """Broadcast statistikasini yangilash"""
    close_old_connections()
    broadcast = Broadcast.objects.get(id=broadcast_id)
    broadcast.sent_count = sent_count
    broadcast.failed_count = failed_count
    broadcast.status = 'completed'
    broadcast.save()

async def send_broadcast(bot: Bot, broadcast_id: int):
    """Broadcast yuborish funksiyasi"""
    broadcast = await get_pending_broadcast()
    
    if not broadcast:
        return
    
    target_users = await get_target_users(broadcast)
    sent_count = 0
    failed_count = 0
    
    for telegram_id in target_users:
        try:
            if broadcast.image:
                photo = FSInputFile(broadcast.image.path)
                await bot.send_photo(
                    chat_id=telegram_id,
                    photo=photo,
                    caption=broadcast.message
                )
            else:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=broadcast.message
                )
            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Broadcast xatosi {telegram_id}: {e}")
        
        # Rate limiting - spamdan saqlanish
        await asyncio.sleep(0.05)  # 50ms kutish
    
    await update_broadcast_stats(broadcast.id, sent_count, failed_count)
    print(f"Broadcast tugadi: {sent_count} yuborildi, {failed_count} xato")
