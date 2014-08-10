# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0008_auto_20140809_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='added',
            field=models.DateTimeField(db_index=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mu',
            name='team',
            field=models.CharField(max_length=1, db_index=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.CharField(max_length=1, db_index=True),
        ),
        migrations.AlterField(
            model_name='portal',
            name='team',
            field=models.CharField(max_length=1, db_index=True),
        ),
    ]
