import time
from pprint import pprint

from django.core.management.base import BaseCommand
from . import utils


class Command(BaseCommand):
    args = 'test ingress collect'
    help = 'test ingress collect'

    def handle(self, *args, **options):
        just_now = int((time.time() - 60) * 1000)
        result = utils.get_plexts(just_now)
        pprint(result)
