# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0007_player_over_lv8'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='health',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='image',
            field=models.CharField(default='', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='image_fetched',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='level',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='mod_status',
            field=models.CharField(default='', max_length=512),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='res_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='res_status',
            field=models.CharField(default='', max_length=512),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='updated',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
