import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot
from apps.bot.bot import run_bot

class Command(BaseCommand):
    help = 'Run Telegram bot (local development - polling mode)'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Bot ishga tushurilmoqda (polling rejimi)...')
        
        # Oldin webhookni o'chirish
        if settings.BOT_TOKEN:
            try:
                self.stdout.write('🔄 Webhookni o\'chirish...')
                bot = Bot(token=settings.BOT_TOKEN)
                asyncio.run(bot.delete_webhook(drop_pending_updates=True))
                self.stdout.write(self.style.SUCCESS('✅ Webhook o\'chirildi'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️ Webhook o\'chirishda xato: {e}'))
        
        # Polling rejimida botni ishga tushir
        self.stdout.write(self.style.SUCCESS('✅ Bot polling rejimida ishga tushdi'))
        run_bot()
