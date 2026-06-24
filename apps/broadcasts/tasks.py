import asyncio
from aiogram import Bot
from django.conf import settings
from apps.users.models import User
from .models import Broadcast

bot = Bot(token=settings.BOT_TOKEN)

async def send_broadcast(broadcast_id):
    """Send broadcast to all users"""
    try:
        broadcast = Broadcast.objects.get(id=broadcast_id)
        broadcast.status = 'sending'
        broadcast.save()
        
        users = User.objects.filter(is_blocked=False)
        
        if not broadcast.target_all:
            # Filter by active subscriptions
            users = users.filter(subscriptions__status='active').distinct()
        
        sent_count = 0
        failed_count = 0
        
        for user in users:
            try:
                if broadcast.image:
                    await bot.send_photo(
                        chat_id=user.telegram_id,
                        photo=broadcast.image,
                        caption=broadcast.message
                    )
                else:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=broadcast.message
                    )
                sent_count += 1
                await asyncio.sleep(0.05)  # Rate limiting
            except Exception as e:
                failed_count += 1
                print(f"Failed to send to {user.telegram_id}: {e}")
        
        broadcast.sent_count = sent_count
        broadcast.failed_count = failed_count
        broadcast.status = 'completed'
        broadcast.save()
        
        return True
    except Exception as e:
        print(f"Broadcast error: {e}")
        broadcast.status = 'failed'
        broadcast.save()
        return False

def start_broadcast(broadcast_id):
    """Start broadcast asynchronously"""
    asyncio.run(send_broadcast(broadcast_id))
