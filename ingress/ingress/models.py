from django.db import models


class Portal(models.Model):
    guid = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=256)
    team = models.CharField(max_length=1)
    owner = models.CharField(max_length=40, blank=True)
    latE6 = models.IntegerField()
    lngE6 = models.IntegerField()
    rlat = models.CharField(max_length=24, default='')
    rlng = models.CharField(max_length=24, default='')
    has_maps = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

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


class Player(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    team = models.CharField(max_length=1)
    portal_count = models.IntegerField(default=0)
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
    added = models.DateTimeField(auto_now_add=True)


class MU(models.Model):
    guid = models.CharField(max_length=64, primary_key=True)
    player = models.ForeignKey('Player')
    points = models.BigIntegerField()
    timestamp = models.BigIntegerField()
    team = models.CharField(max_length=1)
    added = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    guid = models.CharField(max_length=64, primary_key=True)
    text = models.CharField(max_length=512)
    player = models.CharField(max_length=40, blank=True)
    team = models.CharField(max_length=1)
    timestamp = models.BigIntegerField()
    is_secure = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
