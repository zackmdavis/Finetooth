# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 06:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20151020_0507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('published_at',)},
        ),
    ]
