# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-04 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BloggingAPI', '0004_auto_20160331_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(default=b'', max_length=2000, null=True),
        ),
    ]
