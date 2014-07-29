# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0004_portal_has_maps'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('guid', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=512)),
                ('player', models.CharField(max_length=40, blank=True)),
                ('team', models.CharField(max_length=1)),
                ('timestamp', models.BigIntegerField()),
                ('is_secure', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
