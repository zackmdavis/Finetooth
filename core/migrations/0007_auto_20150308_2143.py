# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0006_auto_20141012_0251'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='finetoothuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='finetoothuser',
            name='email',
            field=models.EmailField(blank=True, verbose_name='email address', max_length=254),
        ),
        migrations.RemoveField(
            model_name='finetoothuser',
            name='groups',
        ),
        migrations.AddField(
            model_name='finetoothuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', verbose_name='groups', related_query_name='user'),
        ),
        migrations.AlterField(
            model_name='finetoothuser',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AlterField(
            model_name='finetoothuser',
            name='username',
            field=models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', max_length=30),
        ),
    ]
