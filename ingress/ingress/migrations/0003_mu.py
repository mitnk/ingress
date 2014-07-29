# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0002_action_portal_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='MU',
            fields=[
                ('guid', models.CharField(primary_key=True, serialize=False, max_length=64)),
                ('points', models.BigIntegerField()),
                ('timestamp', models.BigIntegerField()),
                ('team', models.CharField(max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(to='ingress.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
