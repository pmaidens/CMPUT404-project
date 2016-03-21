# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-21 03:35
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=2000)),
                ('url', models.CharField(max_length=2000)),
                ('github', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('bio', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contentType', models.CharField(default=b'text/plain', max_length=255)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='CommentAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.UUIDField()),
                ('host', models.CharField(max_length=2000)),
                ('displayName', models.CharField(max_length=2000)),
                ('url', models.CharField(max_length=2000)),
                ('github', models.CharField(blank=True, default=None, max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author_id', models.UUIDField(default=None)),
                ('host', models.CharField(max_length=2000)),
                ('display_name', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source', models.CharField(default=None, max_length=2000)),
                ('origin', models.CharField(default=None, max_length=2000)),
                ('description', models.TextField(default=None)),
                ('contentType', models.CharField(default=b'text/plain', max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True, default=None, null=True)),
                ('date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=None, max_length=255), blank=True, default=None, size=None)),
                ('visibility', models.CharField(choices=[(b'PUBLIC', b'PUBLIC'), (b'FOAF', b'FOAF'), (b'FRIENDS', b'FRIENDS'), (b'PRIVATE', b'PRIVATE'), (b'SERVERONLY', b'SERVERONLY')], default=b'PUBLIC', max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BloggingAPI.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BloggingAPI.CommentAuthor'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='BloggingAPI.Post'),
        ),
        migrations.AddField(
            model_name='author',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='friendRequestsSent', to='BloggingAPI.Friend'),
        ),
        migrations.AddField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(blank=True, to='BloggingAPI.Friend'),
        ),
        migrations.AddField(
            model_name='author',
            name='pendingFriends',
            field=models.ManyToManyField(blank=True, related_name='friendRequestsRecieved', to='BloggingAPI.Friend'),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]