from django.db import models
from django.core.exceptions import ValidationError
import datetime
from hashlib import sha256
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    
class Agency(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    
class Request(models.Model):
    description = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency)  
    users = models.ManyToManyField(User, related_name="requests")
    creator = models.ForeignKey(User, related_name="created_requests")
    
class Comment(models.Model):
    description = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="comments")
    request = models.ForeignKey(Request, related_name="comments")

