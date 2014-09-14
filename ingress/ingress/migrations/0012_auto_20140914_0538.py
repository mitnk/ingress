# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingress', '0011_portal_has_problem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=40)),
                ('portal_count', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='action',
            name='portal',
            field=models.ForeignKey(null=True, related_name='portal', to='ingress.Portal', blank=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='portal_to',
            field=models.ForeignKey(null=True, related_name='portal_to', to='ingress.Portal', blank=True),
        ),
    ]
