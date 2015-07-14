# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RoutePlanner', '0005_location_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='location1',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='location2',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='location3',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='location4',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='location5',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
