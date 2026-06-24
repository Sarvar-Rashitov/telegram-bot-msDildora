import asyncio
import logging
import django
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings

# Django setup
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from .handlers import start, profile, subscribe, support, callbacks, registration, info
from .middlewares import DatabaseMiddleware
from .states import RegistrationStates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register middlewares
dp.message.middleware(DatabaseMiddleware())

# Register command handlers
dp.message.register(start.cmd_start, Command('start'))

# Register registration handlers (FSM)
dp.message.register(registration.cmd_register, F.text == '📝 Ro\'yxatdan o\'tish')
dp.message.register(registration.process_first_name, RegistrationStates.waiting_for_first_name)
dp.message.register(registration.process_last_name, RegistrationStates.waiting_for_last_name)
dp.message.register(registration.process_phone, RegistrationStates.waiting_for_phone)
dp.message.register(registration.process_age, RegistrationStates.waiting_for_age)
dp.message.register(registration.process_occupation, RegistrationStates.waiting_for_occupation)

# Register main menu handlers
dp.message.register(profile.cmd_profile, F.text == '👤 Profil')
dp.message.register(subscribe.cmd_subscribe, F.text == '💳 Obuna bo\'lish')
dp.message.register(info.cmd_license, F.text == '📄 Litsenziya')
dp.message.register(info.cmd_info, F.text == 'ℹ️ Ma\'lumot')
dp.message.register(info.cmd_help, F.text == '📞 Yordam')

# Register callback handlers
dp.callback_query.register(callbacks.handle_tariff_callback, F.data.startswith('tariff_'))
dp.callback_query.register(callbacks.handle_check_payment, F.data == 'check_payment')

async def start_bot():
    logger.info("Bot ishga tushmoqda...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot xatosi: {e}", exc_info=True)

def run_bot():
    asyncio.run(start_bot())
