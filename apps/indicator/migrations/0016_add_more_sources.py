# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-17 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0015_delete_priceresampled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annpriceclassification',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='eventselementary',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='eventslogical',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='price',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='priceresampl',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='rsi',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='sma',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
        migrations.AlterField(
            model_name='volume',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'poloniex'), (1, 'bittrex'), (2, 'binance'), (3, 'bitfinex'), (4, 'kucoin'), (5, 'gdax'), (6, 'hitbtc')]),
        ),
    ]