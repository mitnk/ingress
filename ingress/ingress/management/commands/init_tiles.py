from django.core.management.base import BaseCommand
from ingress.ingress.models import Tile
from ingress.ingress.utils import get_all_tile_keys


class Command(BaseCommand):
    args = ''
    help = 'Initial tile model'

    def handle(self, *args, **options):
        all_tile_keys = get_all_tile_keys()
        count = 0
        for tile_key in all_tile_keys:
            _, created = Tile.objects.get_or_create(key=tile_key)
            if created:
                count += 1
        print('{} tiles are created'.format(count))
