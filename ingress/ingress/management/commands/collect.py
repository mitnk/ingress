import time
from django.core.management.base import BaseCommand
from ingress.ingress.models import Portal, Action, Player, MU, Message
from . import utils


_D = {
    '_': 0,
    'min_timems': 1406513783823,
}


def get_timems_last_minute():
    try:
        max_timems = Action.objects.order_by('-timestamp')[0].timestamp
        min_timems = _D['min_timems']
        return min_timems if min_timems > max_timems else max_timems
    except:
        return int(time.time() * 1000 - 80 * 1000)


def get_or_create_portal(portal):
    try:
        obj_portal = Portal.objects.get(pk=portal['guid'])
        if obj_portal.team != portal['team'][0]:
            obj_portal.team = portal['team'][0]
            obj_portal.save()
    except Portal.DoesNotExist:
        obj_portal = Portal.objects.create(
            guid=portal['guid'],
            name=portal['name'],
            team=portal['team'][0],
            latE6=portal['latE6'],
            lngE6=portal['lngE6'],
        )
    return obj_portal


class Command(BaseCommand):
    args = ''
    help = 'Collect Ingress Info'

    def handle(self, *args, **options):
        _D['_'] += 1
        if _D['_'] > 10:
            return

        timems = get_timems_last_minute()
        print('===', timems)
        plexts = utils.get_plexts(timems)
        if 'success' not in plexts:
            return
        for item in plexts['success']:
            action = {
                'guid': item[0],
                'timestamp': item[1],
            }
            if _D['min_timems'] < item[1]:
                _D['min_timems'] = item[1]
            if 'plext' not in item[2] \
                    or 'markup' not in item[2]['plext']:
                continue
            markup = item[2]['plext']['markup']

            try:
                text = item[2]['plext']['text']
            except KeyError:
                continue

            player = {}
            portal = {}
            portal_to = {}
            resonator = 0
            is_linking = False
            is_adding_mu = False
            is_secure = False
            mu_points = 0
            for x in markup:
                if x[0] == 'PLAYER':
                    player = {
                        'id': x[1]['plain'],
                        'team': x[1]['team'][0],
                    }
                elif x[0] == 'SECURE':
                    is_secure = True
                elif x[0] == 'SENDER':
                    player = {
                        'id': x[1]['plain'].split(':')[0],
                        'team': x[1]['team'][0],
                    }
                elif x[0] == 'PORTAL':
                    if is_linking:
                        portal_to = x[1]
                    else:
                        portal = x[1]
                elif x[0] == 'TEXT':
                    if 'plain' not in x[1]:
                        continue
                    plain = x[1]['plain']

                    if 'destroyed an' in plain:
                        action['name'] = 'destroyed'
                    elif 'deployed an' in plain:
                        action['name'] = 'deployed'
                    elif 'captured' in plain:
                        action['name'] = 'captured'
                    elif 'created a Control' in plain:
                        action['name'] = 'field'
                    elif 'linked' in plain:
                        action['name'] = 'linked'
                    elif ' to ' == plain:
                        is_linking = True
                    elif ' +' == plain:
                        is_adding_mu = True
                    elif is_adding_mu and plain.isdigit():
                        mu_points = int(plain)
                    elif len(plain) <= 3 and 'L' in plain:
                        resonator = int(plain.strip().replace('L', ''))

            if player and not portal:
                try:
                    obj_player = Player.objects.get(id=player['id'])
                except Player.DoesNotExist:
                    obj_player = Player.objects.create(**player)
                if not Message.objects.filter(guid=action['guid']).exists():
                    Message.objects.create(
                        guid=action['guid'],
                        text=text[:512],
                        player=player['id'],
                        team=player['team'],
                        timestamp=action['timestamp'],
                        is_secure=is_secure,
                    )
                continue

            if not player or not portal:
                continue
            if 'name' not in action:
                continue

            obj_portal = get_or_create_portal(portal)
            if action['name'] == 'captured':
                obj_portal.owner = player['id']
                obj_portal.save()

            if portal_to:
                obj_portal_to = get_or_create_portal(portal_to)
            else:
                obj_portal_to = None

            action['resonator'] = resonator

            try:
                obj_player = Player.objects.get(id=player['id'])
            except Player.DoesNotExist:
                obj_player = Player.objects.create(**player)

            if not Action.objects.filter(pk=action['guid']).exists():
                action['player'] = obj_player
                action['portal'] = obj_portal
                if obj_portal_to:
                    action['portal_to'] = obj_portal_to
                Action.objects.create(**action)

            if action['name'] == 'field':
                if not MU.objects.filter(pk=action['guid']).exists():
                    MU.objects.create(
                        guid=action['guid'],
                        player=obj_player,
                        points=mu_points,
                        timestamp=action['timestamp'],
                        team=obj_player.team
                    )

            info = '{} {} {} {}'.format(player['id'], action['name'], resonator, portal['name'])
            print(info)

        ps = Portal.objects.all()
        print(ps.count())
        ps = Action.objects.all()
        print(ps.count())

        if len(plexts['success']) >= 50:
            self.handle(*args, **options)
