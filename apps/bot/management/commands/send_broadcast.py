from django.core.management.base import BaseCommand
from apps.broadcasts.tasks import start_broadcast

class Command(BaseCommand):
    help = 'Send broadcast message'

    def add_arguments(self, parser):
        parser.add_argument('broadcast_id', type=int, help='Broadcast ID')

    def handle(self, *args, **options):
        broadcast_id = options['broadcast_id']
        self.stdout.write(f'Sending broadcast {broadcast_id}...')
        start_broadcast(broadcast_id)
        self.stdout.write(self.style.SUCCESS('Done!'))
