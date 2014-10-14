# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Yaas', '0004_auto_20141011_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('bidders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='Yaas.Auction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
