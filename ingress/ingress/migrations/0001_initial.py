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
                ('added', models.DateTimeField(db_index=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('guid', models.CharField(max_length=64, serialize=False, primary_key=True)),
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
        migrations.CreateModel(
            name='MU',
            fields=[
                ('guid', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('points', models.BigIntegerField()),
                ('timestamp', models.BigIntegerField()),
                ('team', models.CharField(max_length=1, db_index=True)),
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
                ('team', models.CharField(max_length=1, db_index=True)),
                ('portal_count', models.IntegerField(default=0)),
                ('over_lv8', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('guid', models.CharField(max_length=40, db_index=True)),
                ('name', models.CharField(max_length=256)),
                ('team', models.CharField(max_length=1, db_index=True)),
                ('owner', models.CharField(max_length=40, blank=True)),
                ('latE6', models.IntegerField()),
                ('lngE6', models.IntegerField()),
                ('rlat', models.CharField(max_length=24, default='')),
                ('rlng', models.CharField(max_length=24, default='')),
                ('has_maps', models.BooleanField(default=False)),
                ('level', models.IntegerField(default=0)),
                ('image', models.CharField(max_length=255, default='')),
                ('image_fetched', models.BooleanField(default=False)),
                ('mod_status', models.CharField(max_length=512, default='')),
                ('res_count', models.IntegerField(default=0)),
                ('res_status', models.CharField(max_length=512, default='')),
                ('health', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(null=True)),
                ('last_captured', models.DateTimeField(null=True)),
                ('capture_count', models.IntegerField(default=0)),
                ('has_problem', models.BooleanField(default=False)),
                ('has_real_guid', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('key', models.CharField(max_length=40)),
                ('portal_count', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mu',
            name='player',
            field=models.ForeignKey(to='ingress.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='player',
            field=models.ForeignKey(to='ingress.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='portal',
            field=models.ForeignKey(to='ingress.Portal', related_name='portal', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='portal_to',
            field=models.ForeignKey(to='ingress.Portal', related_name='portal_to', blank=True, null=True),
            preserve_default=True,
        ),
    ]
