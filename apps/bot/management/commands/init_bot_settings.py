from django.core.management.base import BaseCommand
from apps.bot.models import BotSettings

class Command(BaseCommand):
    help = 'Initialize default bot settings'

    def handle(self, *args, **options):
        # License file setting
        BotSettings.objects.get_or_create(
            key='license_file',
            defaults={
                'description': 'Litsenziya shartnomasi PDF fayli',
                'value': ''
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Bot settings initialized'))
