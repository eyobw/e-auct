# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0005_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='state',
            field=models.ForeignKey(to='Yaas.AuctionState', default='1'),
        ),
    ]
