# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0003_mu'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='has_maps',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
