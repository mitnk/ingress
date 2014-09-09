import datetime
import json
import logging
import requests
import time

from urllib.request import urlretrieve
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now
from ingress.ingress.models import Portal

from .utils import HEADERS, cookie_need_update, PAYLOAD_V


class Command(BaseCommand):
    args = ''
    help = 'Fetch portal details'

    def get_payload(self, guid):
        return {
            'b': '',
            'c': '',
            'guid': guid,
            'v': PAYLOAD_V,
        }

    def is_a_bad_portal(self, r):
        return r.status_code != 200

    def get_portal_details(self, po):
        if cookie_need_update():
            logging.error('need to update cookie and others')
            return

        payload = self.get_payload(po.guid)
        try:
            r = requests.post(
                "https://www.ingress.com/r/getPortalDetails",
                data=json.dumps(payload),
                headers=HEADERS
            )
        except:
            logging.exception('Error in get_portal_details():')
            return

        if self.is_a_bad_portal(r):
            po.has_problem = True
            po.save()
            return

        try:
            return json.loads(r.text)
        except:
            logging.exception('')
            logging.info(r.text)

    def handle(self, *args, **options):
        portals = []
        old_datetime = now() - datetime.timedelta(seconds=60 * 60 * 6)
        portals_lv8 = Portal.objects.filter(level=8, updated__lt=old_datetime) \
            .exclude(has_problem=True)
        portals += [x for x in portals_lv8]

        portals_not_updated = Portal.objects.filter(updated=None) \
            .exclude(has_problem=True)[:20]
        portals += [x for x in portals_not_updated]

        portals_oldest = Portal.objects.filter(updated__lt=old_datetime) \
            .exclude(has_problem=True).order_by('updated')[:20]
        portals += [x for x in portals_oldest]

        total = len(portals)
        i = 1
        for po in portals:
            _t = time.time()

            details = self.get_portal_details(po)
            if not details:
                continue
            if details['type'] != 'portal':
                logging.error('detail type error')
                continue

            mod_status = '|'.join(
                ['{}+{}+{}'.format(
                    x['name'], x['rarity'], x['owner']
                 ) for x in details['mods'] if x]
            )

            res_status = '|'.join([
                '{}+{}+{}'.format(x['level'], x['owner'], x['energy'])
                for x in details['resonators'] if x
            ])

            name = details['title']
            latE6 = details['latE6']
            lngE6 = details['lngE6']
            res_count = details['resCount']
            image = details['image']
            health = details['health']
            level = 0 if health == 0 else details['level']
            owner = '' if 'owner' not in details else details['owner']
            team = details['team'][0]

            po.name = name
            po.latE6 = latE6
            po.lngE6 = lngE6
            po.mod_status = mod_status
            po.res_count = res_count
            po.res_status = res_status
            po.health = health
            po.image = image
            po.level = level
            po.owner = owner
            po.team = team
            po.updated = now()
            po.save()

            print('[{}/{}] Got details for {}. time: {:.2f}'.format(
                i, total, po.name, time.time() - _t))
            i += 1
            time.sleep(3.0)
