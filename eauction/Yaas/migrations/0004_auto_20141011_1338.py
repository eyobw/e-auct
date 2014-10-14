# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0003_auto_20141011_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidder',
            name='bidders',
        ),
        migrations.RemoveField(
            model_name='bidder',
            name='item',
        ),
        migrations.DeleteModel(
            name='Bidder',
        ),
    ]
