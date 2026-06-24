from django.core.management.base import BaseCommand
from apps.bot.bot import bot
from apps.bot.handlers.broadcast import send_broadcast
import asyncio

class Command(BaseCommand):
    help = 'Send broadcast message'

    def add_arguments(self, parser):
        parser.add_argument('broadcast_id', type=int, help='Broadcast ID')

    def handle(self, *args, **options):
        broadcast_id = options['broadcast_id']
        self.stdout.write(f'Broadcast yuborilmoqda: {broadcast_id}')
        
        asyncio.run(send_broadcast(bot, broadcast_id))
        
        self.stdout.write(self.style.SUCCESS('✅ Broadcast yuborildi'))
