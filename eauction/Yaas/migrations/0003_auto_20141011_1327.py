# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0002_auto_20141011_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
