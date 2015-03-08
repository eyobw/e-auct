# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0011_auto_20141017_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='bidder_name',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='bidder'),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='item',
            field=models.ForeignKey(to='Yaas.Auction', related_name='bidders'),
        ),
    ]
