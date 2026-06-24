import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings

from .handlers import start, profile, subscribe, support, callbacks
from .middlewares import DatabaseMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register middlewares
dp.message.middleware(DatabaseMiddleware())

# Register message handlers
dp.message.register(start.cmd_start, Command('start'))
dp.message.register(profile.cmd_profile, F.text == '👤 Profil')
dp.message.register(subscribe.cmd_subscribe, F.text == '💳 Obuna bo\'lish')
dp.message.register(support.cmd_support, F.text == '📞 Yordam')

# Register callback handlers
dp.callback_query.register(callbacks.handle_tariff_callback, F.data.startswith('tariff_'))
dp.callback_query.register(callbacks.handle_check_payment, F.data == 'check_payment')

async def start_bot():
    logger.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

def run_bot():
    asyncio.run(start_bot())
