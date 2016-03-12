import uuid
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from datetime import datetime
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    #set the user to non active and have admin approve
    user.is_active = False
    user.save()


class Author(models.Model):
    user = models.OneToOneField(User)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # profile_img = models.ImageField(default=None)
    host = models.CharField(max_length=2000)
    url = models.CharField(max_length=2000)
    friends = models.ManyToManyField('Friend', blank=True)
    pendingFriends = models.ManyToManyField('Friend',related_name='friendReq', blank=True)
    github = models.CharField(max_length=2000, default=None, blank=True, null=True)
    bio = models.TextField(default=None, blank=True, null=True)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            #set the host to current domain and url to host/author/id
            generated_id = uuid.uuid4()
            current_host = Site.objects.get_current().domain
            author_url = current_host + '/author/' + str(generated_id)
            Author.objects.get_or_create(user=instance, id=generated_id, host=current_host, url=author_url)

    post_save.connect(create_user_profile, sender=User)

class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.UUIDField(default=None)
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
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    categories = ArrayField(models.CharField(default=None, max_length=255, blank=True), default=None, blank=True)
    #image = models.ImageField(default=None)
    visibility = models.CharField(default='PUBLIC', max_length=255, choices=visibility_choices)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author)
    contentType = models.CharField(default='text/plain', max_length=255)
    comment = models.TextField(default=None, blank=True, null=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
