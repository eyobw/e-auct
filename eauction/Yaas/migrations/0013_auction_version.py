# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0012_auto_20141101_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
