import time
from urllib.request import urlretrieve
from django.core.management.base import BaseCommand
from django.conf import settings
from ingress.ingress.models import Portal


class Command(BaseCommand):
    args = ''
    help = 'Fetch portal images'

    def save_image(self, url, path):
        urlretrieve(url, path)

    def get_image_path(self, po):
        path = settings.DIR_PORTAL_MAPS.rstrip('/') + '/{}_{}.jpg'
        return path.format(po.guid, 'image')

    def handle(self, *args, **options):
        portals = Portal.objects.filter(
            image_fetched=False,
        ).exclude(image='')[:20]
        total = portals.count()
        i = 1
        for po in portals:
            _t = time.time()

            image_path = self.get_image_path(po)
            self.save_image(po.image, image_path)
            po.image_fetched = True
            po.save()

            print('[{}/{}] Got portal image for {}. time: {:.2f}'.format(
                i, total, po.name, time.time() - _t))
            i += 1
            time.sleep(3.0)
