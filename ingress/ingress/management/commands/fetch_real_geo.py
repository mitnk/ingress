import json
from urllib.request import urlopen
from django.core.management.base import BaseCommand
from django.conf import settings
from ingress.ingress.models import Portal


class Command(BaseCommand):
    args = ''
    help = 'Fetch map images for protals'

    url = 'http://api.map.baidu.com/geoconv/v1/?coords={},{}&from=1&to=5&ak={}'

    def get_url(self, po):
        url = self.url.format(
            po.get_lng(),
            po.get_lat(),
            settings.BAIDU_APP_SECRET_KEY,
        )
        return url

    def get_real_geo(self, geo_str):
        geo = json.loads(geo_str.decode('utf-8'))
        return geo['result'][0]

    def handle(self, *args, **options):
        portals = Portal.objects.filter(rlat='', rlng='').order_by('-added')[:500]
        total = portals.count()
        i = 1
        for po in portals:
            print('[{}/{}] Get geo for {}'.format(i, total, po.name))
            i += 1
            url = self.get_url(po)
            content = urlopen(url).read().strip()
            geo = self.get_real_geo(content)
            po.rlat = geo.get('y', '')
            po.rlng = geo.get('x', '')
            po.save()
