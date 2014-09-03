# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 3, 3, 57, 44, 517051), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 3, 3, 57, 54, 173017)),
            preserve_default=False,
        ),
    ]
