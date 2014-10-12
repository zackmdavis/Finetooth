# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify
from django.db import models, migrations


def slugify_migrate_forward(apps, schema_editor):
    Post = apps.get_model('core', "Post")
    for post in Post.objects.all():
        post.slug = slugify(post.title)
        post.save()

def unslugify_migrate_backward(apps, schema_editor):
    Post = apps.get_model('core', "Post")
    for post in Post.objects.all():
        post.slug = None
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_post_slug'),
    ]

    operations = [
        migrations.RunPython(slugify_migrate_forward, unslugify_migrate_backward)
    ]
