# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-15 06:27
from __future__ import unicode_literals

from django.db import migrations
import unixtimestampfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('signal', '0003_auto_20171113_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='sent_at',
            field=unixtimestampfield.fields.UnixTimeStampField(default=0),
            preserve_default=False,
        ),
    ]