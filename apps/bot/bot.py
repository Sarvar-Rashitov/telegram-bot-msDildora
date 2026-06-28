import asyncio
import logging
import django
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, MEMBER, KICKED, StateFilter
from aiogram.types import Message, ChatMemberUpdated
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from django.conf import settings

# Django setup
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from .handlers import start, profile, subscribe, support, callbacks, registration, info, channel
from .middlewares import DatabaseMiddleware
from .states import RegistrationStates, SupportTicketStates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register middlewares
dp.message.middleware(DatabaseMiddleware())

# Register command handlers (highest priority - work in any state)
dp.message.register(start.cmd_start, Command('start'))

# Register FSM state handlers - Registration
dp.message.register(registration.process_first_name, RegistrationStates.waiting_for_first_name)
dp.message.register(registration.process_last_name, RegistrationStates.waiting_for_last_name)
dp.message.register(registration.process_phone, RegistrationStates.waiting_for_phone)
dp.message.register(registration.process_age, RegistrationStates.waiting_for_age)
dp.message.register(registration.process_occupation, RegistrationStates.waiting_for_occupation)

# Register FSM state handlers - Support Ticket
dp.message.register(support.process_ticket_subject, SupportTicketStates.waiting_for_subject)
dp.message.register(support.process_ticket_message, SupportTicketStates.waiting_for_message)

# Register main menu handlers (only when no FSM state is active)
dp.message.register(registration.cmd_register, F.text == '📝 Ro\'yxatdan o\'tish', StateFilter(None))
dp.message.register(support.cmd_create_ticket, F.text == '✍️ Murojaat qoldirish', StateFilter(None))
dp.message.register(profile.cmd_profile, F.text == '👤 Profil', StateFilter(None))
dp.message.register(subscribe.cmd_subscribe, F.text == '💳 Obuna bo\'lish', StateFilter(None))
dp.message.register(channel.cmd_join_channel, F.text == '📢 Kanalga o\'tish', StateFilter(None))
dp.message.register(info.cmd_license, F.text == '📄 Litsenziya', StateFilter(None))
dp.message.register(info.cmd_info, F.text == 'ℹ️ Ma\'lumot', StateFilter(None))
dp.message.register(support.cmd_help, F.text == '📞 Yordam', StateFilter(None))

# Debug handler - catch all unhandled messages
@dp.message(StateFilter(None))
async def debug_unhandled(message: Message):
    logger.warning(f"⚠️ Unhandled message: '{message.text}' from {message.from_user.id}")
    await message.answer(
        f"🔍 Debug info:\n"
        f"Text: '{message.text}'\n"
        f"User: {message.from_user.id}\n"
        f"Handler topilmadi!"
    )

# Register callback handlers
dp.callback_query.register(callbacks.handle_tariff_callback, F.data.startswith('tariff_'))
dp.callback_query.register(callbacks.handle_check_payment, F.data == 'check_payment')
dp.callback_query.register(support.handle_create_ticket_callback, F.data == 'create_ticket')

# Register chat member handler (kanalga kirishni tekshirish)
dp.chat_member.register(
    lambda event: channel.check_chat_member(event, bot),
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)

async def start_bot_polling():
    """Bot polling rejimida (development)"""
    logger.info("🚀 Bot polling rejimida ishga tushmoqda...")
    logger.info(f"📋 Handler registratsiyasi: {len(dp.message.handlers)} message, {len(dp.callback_query.handlers)} callback")
    
    try:
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query', 'chat_member'])
    except Exception as e:
        logger.error(f"❌ Bot xatosi: {e}", exc_info=True)

def run_bot():
    """Polling rejimida botni ishga tushirish"""
    asyncio.run(start_bot_polling())
