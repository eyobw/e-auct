# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0009_bidder_bidder_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='price_min',
            field=models.DecimalField(max_digits=10, default=0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='price',
            field=models.DecimalField(max_digits=10, default=0, decimal_places=2),
        ),
    ]
