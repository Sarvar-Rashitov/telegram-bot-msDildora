from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bot'
    verbose_name = 'Telegram Bot'

