import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.bot.models import BotSettings

# Zarur sozlamalarni yaratish
settings_data = [
    {
        'key': 'license',
        'value': 'test-license-key',
        'description': 'Bot litsenziya kaliti'
    },
    {
        'key': 'welcome_text',
        'value': 'Xush kelibsiz!',
        'description': 'Bot boshida ko\'rsatiladigan matn'
    },
    {
        'key': 'help_text',
        'value': 'Yordam uchun /help buyruqni kiriting',
        'description': 'Yordam matni'
    }
]

for setting_data in settings_data:
    obj, created = BotSettings.objects.get_or_create(
        key=setting_data['key'],
        defaults={
            'value': setting_data['value'],
            'description': setting_data['description']
        }
    )
    if created:
        print(f"✓ Sozlama yaratildi: {setting_data['key']}")
    else:
        print(f"✗ Sozlama allaqachon bor: {setting_data['key']}")
