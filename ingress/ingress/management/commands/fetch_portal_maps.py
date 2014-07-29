import time
from urllib.request import urlretrieve
from django.core.management.base import BaseCommand
from django.conf import settings
from ingress.ingress.models import Portal


class Command(BaseCommand):
    args = ''
    help = 'Fetch map images for protals'

    url = 'http://maps.googleapis.com/maps/api/staticmap' \
          '?markers=color:red%7Clabel:P%7C{},{}' \
          '&center={},{}&zoom={}&size=400x400&key={}'

    url_cn = 'http://api.map.baidu.com/staticimage?' \
        'center={},{}&width=400&height=400&zoom={}' \
        '&markers={},{}&markerStyles=l,P,red'

    def get_cn_map_url(self, po, zoom):
        url = self.url_cn.format(
            po.get_cn_lng(),
            po.get_cn_lat(),
            zoom,
            po.get_cn_lng(),
            po.get_cn_lat(),
        )
        return url

    def get_map_url(self, po, zoom, satellite=False):
        if satellite:
            url = self.url.format(
                po.get_lat(),
                po.get_lng(),
                po.get_lat(),
                po.get_lng(),
                zoom,
                settings.GOOGLE_APP_SECRET_KEY,
            )
            url += '&maptype=satellite'
        else:
            url = self.url.format(
                po.get_cn_lat(),
                po.get_cn_lng(),
                po.get_cn_lat(),
                po.get_cn_lng(),
                zoom,
                settings.GOOGLE_APP_SECRET_KEY,
            )
        return url

    def get_map_path(self, po, typ):
        path = settings.DIR_PORTAL_MAPS.rstrip('/') + '/{}_{}.png'
        return path.format(po.guid, typ)

    def save_image(self, url, path):
        urlretrieve(url, path)

    def handle(self, *args, **options):
        portals = Portal.objects.filter(has_maps=False).exclude(rlat='').order_by('-added')[:100]
        total = portals.count()
        i = 1
        for po in portals:
            _t = time.time()
            map_out_url = self.get_cn_map_url(po, 12)
            map_out_path = self.get_map_path(po, 'out')
            self.save_image(map_out_url, map_out_path)

            map_in_url = self.get_cn_map_url(po, 16)
            map_in_path = self.get_map_path(po, 'in')
            self.save_image(map_in_url, map_in_path)

            map_in_satellite_url = self.get_map_url(po, 16, satellite=True)
            map_in_satellite_path = self.get_map_path(po, 'in_sat')
            self.save_image(map_in_satellite_url, map_in_satellite_path)
            po.has_maps = True
            po.save()

            print('[{}/{}] Got maps for {}. time: {:.2f}'.format(i, total, po.name, time.time() - _t))
            i += 1
