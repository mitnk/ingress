# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='portal_to',
            field=models.ForeignKey(null=True, to='ingress.Portal', blank=True),
            preserve_default=True,
        ),
    ]
