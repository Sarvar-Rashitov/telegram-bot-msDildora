from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, Update
import django
import os
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware Django database ulanishlarini to'g'ri boshqaradi.
    Django ORM operatsiyalarini async kontekstda ishlatsak ham saqlaydi.
    """
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Handler o'z ichida sync_to_async ishlatadi, bu yerda biz faqat
        # handler'ni chaqiramiz va async kontekstda ishlashiga ruxsat beramiz
        try:
            return await handler(event, data)
        except Exception as e:
            # Xatolikni log qilish
            import logging
            logging.error(f"Middleware xatosi: {e}", exc_info=True)
            raise
