from aiogram import Bot
from django.conf import settings

bot = Bot(token=settings.BOT_TOKEN)

async def add_user_to_channel(user_telegram_id, channel_id):
    """Add user to private channel"""
    try:
        # Create invite link for user
        invite_link = await bot.create_chat_invite_link(
            chat_id=channel_id,
            member_limit=1
        )
        return invite_link.invite_link
    except Exception as e:
        print(f"Error adding user to channel: {e}")
        return None

async def remove_user_from_channel(user_telegram_id, channel_id):
    """Remove user from private channel"""
    try:
        await bot.ban_chat_member(chat_id=channel_id, user_id=user_telegram_id)
        await bot.unban_chat_member(chat_id=channel_id, user_id=user_telegram_id)
        return True
    except Exception as e:
        print(f"Error removing user from channel: {e}")
        return False

async def approve_join_request(user_telegram_id, channel_id):
    """Approve user's join request to channel"""
    try:
        await bot.approve_chat_join_request(
            chat_id=channel_id,
            user_id=user_telegram_id
        )
        return True
    except Exception as e:
        print(f"Error approving join request: {e}")
        return False
