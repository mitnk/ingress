import os.path
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
        portals = Portal.objects.filter(
            has_maps=False,
        ).exclude(rlat='').order_by('-added')[:100]
        total = portals.count()
        if total == 0:
            print('No portals need to fetch maps')
            return

        i = 1
        for po in portals:
            _t = time.time()
            image_path = self.get_map_path(po, 'out')
            if os.path.exists(image_path) \
                    and os.path.getsize(image_path) > 2000:
                print('{} already has out map image, ignored'.format(po.name))
            else:
                map_out_url = self.get_cn_map_url(po, 12)
                self.save_image(map_out_url, image_path)

            image_path = self.get_map_path(po, 'in')
            if os.path.exists(image_path) \
                    and os.path.getsize(image_path) > 2000:
                print('{} already has out map image, ignored'.format(po.name))
            else:
                map_in_url = self.get_cn_map_url(po, 16)
                self.save_image(map_in_url, image_path)

            image_path = self.get_map_path(po, 'in_sat')
            if os.path.exists(image_path) \
                    and os.path.getsize(image_path) > 2000:
                print('{} already has out map image, ignored'.format(po.name))
            else:
                map_in_satellite_url = self.get_map_url(po, 16, satellite=True)
                self.save_image(map_in_satellite_url, image_path)

            po.has_maps = True
            po.save()

            print('[{}/{}] Got maps for {}. time: {:.2f}'.format(i, total, po.name, time.time() - _t))
            i += 1
