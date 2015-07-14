# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RoutePlanner', '0006_auto_20150713_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='userprofile',
            field=models.ForeignKey(blank=True, to='RoutePlanner.UserProfile', null=True),
            preserve_default=True,
        ),
    ]
