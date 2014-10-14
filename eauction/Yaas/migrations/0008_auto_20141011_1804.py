# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0007_auto_20141011_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidder',
            name='bidders',
        ),
        migrations.AlterField(
            model_name='bidder',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
