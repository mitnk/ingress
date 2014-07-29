# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('guid', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('resonator', models.IntegerField(default=0)),
                ('timestamp', models.BigIntegerField()),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('team', models.CharField(max_length=1)),
                ('portal_count', models.IntegerField(default=0)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='action',
            name='player',
            field=models.ForeignKey(to='ingress.Player'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('guid', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('team', models.CharField(max_length=1)),
                ('owner', models.CharField(max_length=40, blank=True)),
                ('latE6', models.IntegerField()),
                ('lngE6', models.IntegerField()),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='action',
            name='portal',
            field=models.ForeignKey(blank=True, null=True, to='ingress.Portal'),
            preserve_default=True,
        ),
    ]
