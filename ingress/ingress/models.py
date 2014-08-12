import datetime
from django.db import models
from django.utils.timezone import now


class Portal(models.Model):
    guid = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=256)
    team = models.CharField(max_length=1, db_index=True)
    owner = models.CharField(max_length=40, blank=True)
    latE6 = models.IntegerField()
    lngE6 = models.IntegerField()
    rlat = models.CharField(max_length=24, default='')
    rlng = models.CharField(max_length=24, default='')
    has_maps = models.BooleanField(default=False)

    level = models.IntegerField(default=0)
    image = models.CharField(max_length=255, default='')
    image_fetched = models.BooleanField(default=False)

    mod_status = models.CharField(max_length=512, default='')
    res_count = models.IntegerField(default=0)
    res_status = models.CharField(max_length=512, default='')
    health = models.IntegerField(default=0)
    updated = models.DateTimeField(null=True)

    last_captured = models.DateTimeField(null=True)
    capture_count = models.IntegerField(default=0)

    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/portals/{}/'.format(self.guid)

    def get_hold_days(self):
        if self.last_captured:
            return 0
        return (self.last_captured - now()).days

    def mod_list(self):
        result = []
        for s in self.mod_status.split('|'):
            if not s:
                break
            name, rarity, owner = s.split('+')
            result.append({
                'name': name,
                'rarity': rarity.replace(' ', '_'),
                'owner': owner,
            })
        while len(result) < 4:
            result.append({'rarity': 'empty'})
        return result

    def resolator_list(self):
        result = []
        for s in self.res_status.split('|'):
            if not s:
                break
            level, owner, _ = s.split('+')
            result.append({
                'level': level,
                'owner': owner,
            })
        while len(result) < 8:
            result.append({'team': 'empty'})
        return result

    def get_lat(self):
        return '{:.6f}'.format(self.latE6 / 1000000)

    def get_lng(self):
        return '{:.6f}'.format(self.lngE6 / 1000000)

    def get_cn_lat(self):
        if not self.rlat:
            return ''
        return '{:.6f}'.format(float(self.rlat))

    def get_cn_lng(self):
        if not self.rlng:
            return ''
        return '{:.6f}'.format(float(self.rlng))

    def updated_str(self):
        if not self.updated:
            return "NEVER"

        span =  now() - self.updated
        days = span.days
        seconds = span.seconds
        if days >= 6:
            return self.updated.strftime('%Y-%m-%d')
        elif days > 1:
            return '{} days ago'.format(days)
        elif days == 1:
            return '1 day ago'
        elif seconds >= 3600 * 2:
            return '{} hours ago'.format(seconds // 3600)
        elif seconds >= 3600:
            return '1 hour ago'
        elif seconds >= 60 * 2:
            return '{} mins ago'.format(seconds // 60)
        elif seconds >= 60:
            return '1 min ago'
        elif seconds > 1:
            return '{} secs ago'.format(seconds)
        else:
            return '1 sec ago'


class Player(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    team = models.CharField(max_length=1, db_index=True)
    portal_count = models.IntegerField(default=0)
    over_lv8 = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.id


class Action(models.Model):
    guid = models.CharField(max_length=64, primary_key=True)
    player = models.ForeignKey('Player')
    name = models.CharField(max_length=40)
    resonator = models.IntegerField(default=0)
    portal = models.ForeignKey('Portal', null=True, blank=True, related_name='portal')
    portal_to = models.ForeignKey('Portal', null=True, blank=True, related_name='portal_to')
    timestamp = models.BigIntegerField()
    added = models.DateTimeField(auto_now_add=True, db_index=True)

    def hour_minute(self):
        d = datetime.datetime.utcfromtimestamp(self.timestamp // 1000)
        span =  now().replace(tzinfo=None) - d
        days = span.days
        seconds = span.seconds
        if days >= 6:
            return d.strftime('%Y-%m-%d')
        elif days > 1:
            return '{} days ago'.format(days)
        elif days == 1:
            return '1 day ago'
        elif seconds >= 3600 * 2:
            return '{} hours ago'.format(seconds // 3600)
        elif seconds >= 3600:
            return '1 hour ago'
        elif seconds >= 60 * 2:
            return '{} mins ago'.format(seconds // 60)
        elif seconds >= 60:
            return '1 min ago'
        elif seconds > 1:
            return '{} secs ago'.format(seconds)
        else:
            return '1 sec ago'


class MU(models.Model):
    guid = models.CharField(max_length=64, primary_key=True)
    player = models.ForeignKey('Player')
    points = models.BigIntegerField()
    timestamp = models.BigIntegerField()
    team = models.CharField(max_length=1, db_index=True)
    added = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    guid = models.CharField(max_length=64, primary_key=True)
    text = models.CharField(max_length=512)
    player = models.CharField(max_length=40, blank=True)
    team = models.CharField(max_length=1)
    timestamp = models.BigIntegerField()
    is_secure = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
