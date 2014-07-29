# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='rlat',
            field=models.CharField(max_length=24, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='portal',
            name='rlng',
            field=models.CharField(max_length=24, default=''),
            preserve_default=True,
        ),
    ]
