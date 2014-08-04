# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0006_auto_20140726_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='over_lv8',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
