# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-17 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangedata',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
    ]
