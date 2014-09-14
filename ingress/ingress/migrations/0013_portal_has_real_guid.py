# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0012_auto_20140914_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='has_real_guid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
