# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0010_auto_20140812_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='has_problem',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
