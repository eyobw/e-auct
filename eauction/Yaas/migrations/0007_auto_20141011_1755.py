# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0006_auto_20141011_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='price_max',
        ),
        migrations.AddField(
            model_name='bidder',
            name='price',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),

    ]
