# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('Yaas', '0010_auto_20141017_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='price_min',
            field=models.DecimalField(max_digits=10, default=0, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], decimal_places=2),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='price',
            field=models.DecimalField(max_digits=10, default=0, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], decimal_places=2),
        ),
    ]
