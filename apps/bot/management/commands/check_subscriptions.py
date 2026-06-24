from django.core.management.base import BaseCommand
from apps.subscriptions.scheduler import check_expiring_subscriptions

class Command(BaseCommand):
    help = 'Check and update expiring subscriptions'

    def handle(self, *args, **options):
        self.stdout.write('Checking subscriptions...')
        check_expiring_subscriptions()
        self.stdout.write(self.style.SUCCESS('Done!'))
