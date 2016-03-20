# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-20 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BloggingAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='friendRequestsSent', to='BloggingAPI.Friend'),
        ),
        migrations.AlterField(
            model_name='author',
            name='pendingFriends',
            field=models.ManyToManyField(blank=True, related_name='friendRequestsRecieved', to='BloggingAPI.Friend'),
        ),
    ]