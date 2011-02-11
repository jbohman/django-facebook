from django.db import models
from django.contrib.auth.models import User

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class FacebookProfile(models.Model):
    user        = models.ForeignKey(User)
    uid         = models.CharField(max_length=31)
    name        = models.CharField(max_length=100)
    first_name  = models.CharField(max_length=31)
    middle_name = models.CharField(max_length=31, null=True, blank=True)
    last_name   = models.CharField(max_length=31)
    link        = models.URLField(null=True, blank=True)
    birthday    = models.DateField(null=True, blank=True)
    hometown    = models.CharField(max_length=31, null=True, blank=True)
    bio         = models.TextField(null=True, blank=True)
    gender      = models.CharField(max_length=1, choices=GENDERS, null=True, blank=True)
    modified    = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % (self.name)

class FacebookFriend(models.Model):
    friend_of = models.ForeignKey(FacebookProfile)
    name      = models.CharField(max_length=100)
    uid       = models.CharField(max_length=31)

    class Meta:
        unique_together = (('friend_of', 'uid'),)
