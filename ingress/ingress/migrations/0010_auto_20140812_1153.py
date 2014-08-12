# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0009_auto_20140810_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='capture_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='last_captured',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
