# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tile',
            name='n_po_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tile',
            name='portal',
            field=models.ForeignKey(related_name='tile_portal', blank=True, to='ingress.Portal', null=True),
            preserve_default=True,
        ),
    ]
