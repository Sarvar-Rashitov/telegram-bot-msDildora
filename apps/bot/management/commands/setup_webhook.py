import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from aiogram import Bot

class Command(BaseCommand):
    help = 'Setup Telegram webhook'

    def handle(self, *args, **options):
        if not settings.BOT_TOKEN or not settings.BOT_WEBHOOK_URL:
            self.stdout.write(self.style.ERROR('❌ BOT_TOKEN yoki BOT_WEBHOOK_URL sozlanmagan'))
            return

        try:
            self.stdout.write(f'🔄 Webhook sozlanmoqda: {settings.BOT_WEBHOOK_URL}')
            asyncio.run(self._setup(settings.BOT_TOKEN, settings.BOT_WEBHOOK_URL))
            self.stdout.write(self.style.SUCCESS('✅ Webhook sozlandi'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Xato: {e}'))

    async def _setup(self, token, url):
        bot = Bot(token=token)
        await bot.set_webhook(
            url=url,
            allowed_updates=['message', 'callback_query', 'chat_member'],
            drop_pending_updates=False
        )
        info = await bot.get_webhook_info()
        print(f'Webhook URL: {info.url}')
        print(f'Pending updates: {info.pending_update_count}')
        await bot.session.close()
