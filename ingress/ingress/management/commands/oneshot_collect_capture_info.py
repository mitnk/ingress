import time
from urllib.request import urlretrieve
from django.core.management.base import BaseCommand
from django.conf import settings
from ingress.ingress.models import Portal, Action


class Command(BaseCommand):
    args = ''
    help = 'Fetch portal images'

    def save_image(self, url, path):
        urlretrieve(url, path)

    def get_image_path(self, po):
        path = settings.DIR_PORTAL_MAPS.rstrip('/') + '/{}_{}.jpg'
        return path.format(po.guid, 'image')

    def handle(self, *args, **options):
        portals = Portal.objects.all()
        total = portals.count()
        i = 1
        for po in portals:
            _t = time.time()

            act_list = Action.objects.filter(
                portal=po,
                name='captured'
            )
            po.capture_count = act_list.count()
            try:
                latest_one = act_list.order_by('-added')[0]
                # XXX: not that accuracy here, should use timestamp
                po.last_captured = latest_one.added
            except:
                pass
            po.save()

            print('[{}/{}] Got portal capture info for {}. time: {:.2f}'.format(
                i, total, po.name, time.time() - _t))
            i += 1
