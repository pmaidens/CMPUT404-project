import uuid
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.postgres.fields import ArrayField
# from django.db.models.signals import post_save

class Author(models.Model):
    user = models.OneToOneField(User)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # profile_img = models.ImageField(default=None)
    host = models.CharField(max_length=2000, blank=False)
    url = models.CharField(max_length=2000, blank=False)
    friends = models.ManyToManyField('Friend', blank=True)
    github = models.CharField(max_length=2000, default=None, blank=True, null=True)
    bio = models.TextField(default=None, blank=True, null=True)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.get_or_create(user=instance)

    # post_save.connect(create_user_profile, sender=User)

class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=2000, blank=False)
    display_name = models.CharField(max_length=30, blank=False)
    url = models.CharField(max_length=2000, blank=False)

class Post(models.Model):

    visibility_choices = (
        ('PUBLIC', 'PUBLIC'),
        ('FOAF', 'FOAF'),
        ('FRIENDS', 'FRIENDS'),
        ('PRIVATE', 'PRIVATE'),
        ('SERVERONLY', 'SERVERONLY'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author)
    source = models.CharField(default=None, max_length=2000)
    origin = models.CharField(default=None, max_length=2000)
    description = models.TextField(default=None)
    contentType = models.CharField(default='text/plain', max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField(default=None, blank=True, null=True)
    date_created = models.DateField()
    categories = ArrayField(models.CharField(default=None, max_length=255), default=None)
    #image = models.ImageField(default=None)
    visibility = models.CharField(default='PUBLIC', max_length=255, choices=visibility_choices)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, default=None, null=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author)
    contentType = models.CharField(default='text/plain', max_length=255)
    comment = models.TextField(default=None, blank=True, null=True)