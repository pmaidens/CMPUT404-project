# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-31 00:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BloggingAPI', '0003_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='display_name',
            new_name='displayName',
        ),
    ]
