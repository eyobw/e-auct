# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Yaas', '0008_auto_20141011_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidder',
            name='bidder_name',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default='1'),
            preserve_default=False,
        ),
    ]
