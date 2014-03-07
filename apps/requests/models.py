from django.db import models
from django.core.exceptions import ValidationError
import datetime
from hashlib import sha256
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    blocked = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    
class Agency(models.Model):
    a_name = models.CharField(max_length=255, blank=True, unique=True)
    email = models.EmailField(max_length=255)
    def __unicode__(self):
        return self.a_name
    
class Request(models.Model):
    STATE_CHOICES = (
        ('pending', "Pending"),
        ('resolved', "Resolved"),
        ('denied', "Denied")
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency, related_name="requests", null=True, blank=True)  
    users = models.ManyToManyField(User, related_name="requests")
    creator = models.ForeignKey(User, related_name="created_requests")
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')
    def __unicode__(self):
        return self.title
    
class Comment(models.Model):
    description = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="comments")
    request = models.ForeignKey(Request, related_name="comments")
    def __unicode__(self):
        return self.description[:80]

