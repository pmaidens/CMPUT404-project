import uuid
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save

class Author(models.Model):
    user = models.OneToOneField(User)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # profile_img = models.ImageField(default=None)
    host = models.CharField(max_length=2000, blank=False)
    url = models.CharField(max_length=2000, blank=False)
    github = models.CharField(max_length=2000, default=None, blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

class Post(models.Model):

    visibility_choices = (
        ('PUBLIC', 'PUBLIC'),
        ('FOAF', 'FOAF'),
        ('FRIENDS', 'FRIENDS'),
        ('PRIVATE', 'PRIVATE'),
        ('SERVERONLY', 'SERVERONLY'),
    )

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author)
    source = models.CharField(default=None, max_length=2000)
    origin = models.CharField(default=None, max_length=2000)
    description = models.TextField(default=None)
    contentType = models.CharField(default='text/plain', max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField(default=None, blank=True, null=True)
    date_created = models.DateField()
    categories = ArrayField(models.CharField(default=None, max_length=255), default=None)
    image = models.ImageField(default=None)
    count = models.IntegerField(default=None)
    visibility = models.CharField(default='PUBLIC', max_length=255, choices=visibility_choices)


class Comment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author)
    contentType = models.CharField(default='text/plain', max_length=255)
    comment = models.TextField(default=None, blank=True, null=True)
    parent_post = models.ForeignKey(Post)
