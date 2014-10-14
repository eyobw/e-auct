# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Yaas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='Yaas.Auction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='auction',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 11, 13, 3, 58, 56554)),
        ),
        migrations.AlterField(
            model_name='auction',
            name='state',
            field=models.ForeignKey(to='Yaas.AuctionState', default='1'),
        ),
    ]
