import datetime
import json
import logging
import requests
import time

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from ingress.ingress.models import Portal, Tile
from ingress.ingress.utils import within_range

from .utils import HEADERS, cookie_need_update, PAYLOAD_V


def get_or_create_portal(portal):
    try:
        obj_portal = Portal.objects.get(
            latE6=portal['latE6'],
            lngE6=portal['lngE6'],
            has_problem=False,
        )
        obj_portal.name=portal['name']
        obj_portal.team=portal['team'][0]
        obj_portal.latE6=portal['latE6']
        obj_portal.lngE6=portal['lngE6']
        obj_portal.level=portal['level']
        obj_portal.image=portal['image']
        obj_portal.has_real_guid = True
        obj_portal.save()
    except Portal.DoesNotExist:
        obj_portal = Portal.objects.create(
            guid=portal['guid'],
            name=portal['name'],
            team=portal['team'][0],
            latE6=portal['latE6'],
            lngE6=portal['lngE6'],
            level=portal['level'],
            image=portal['image'],
            has_real_guid = True,
        )
    return obj_portal


def get_payload(tileKeys):
    return {
        'b': '',
        'c': '',
        'tileKeys': tileKeys,
        'v': PAYLOAD_V,
    }


def get_entities():
    old_datetime = now() - datetime.timedelta(seconds=60 * 60 * 24)
    tiles = Tile.objects.filter(updated__lt=old_datetime).order_by('updated')[:3]
    if not tiles:
        return

    tileKeys = [x.key for x in tiles]
    payload = get_payload(tileKeys)

    try:
        r = requests.post(
                "https://www.ingress.com/r/getEntities",
            data=json.dumps(payload),
            headers=HEADERS
        )
    except:
        logging.exception('Error in get_entities():')
        return

    try:
        result = json.loads(r.text)
    except:
        logging.exception('')
        logging.error(r.text)
        return

    count_info = {}
    tiles_dict = result['result']['map']
    for tile_key, value in tiles_dict.items():
        if 'error' in value:
            logging.error('Error {} found for tile: {}'.format(value['error'], tile_key))
            continue
        if 'gameEntities' not in value:
            logging.error('No gameEntities found for tile: {}'.format(tile_key))
            continue

        portal_count = 0
        print('==========' + tile_key + '========')
        entities = value['gameEntities']
        for item in entities:
            entity = item[2]
            if entity['type'] != 'portal':
                continue
            portal_count += 1

            guid = item[0]
            latE6 = entity['latE6']
            lngE6 = entity['lngE6']
            if not within_range(latE6, lngE6):
                continue
            name = entity['title']
            team = entity['team']
            portal = {}
            portal['guid'] = guid
            portal['name'] = entity['title']
            portal['team'] = entity['team']
            portal['latE6'] = entity['latE6']
            portal['lngE6'] = entity['lngE6']
            portal['level'] = entity['level']
            portal['image'] = entity['image']
            obj_portal = get_or_create_portal(portal)
            print('- ' + name + ' ' + guid + ' ' + team)
        count_info[tile_key] = portal_count

    # update last updated flag
    for tile in tiles:
        tile.portal_count = count_info.get(tile.key, 0)
        tile.save()


class Command(BaseCommand):
    args = ''
    help = 'Fetch portals base on map tiles'


    def handle(self, *args, **options):
        for i in range(4):
            get_entities()
            time.sleep(1.0)
