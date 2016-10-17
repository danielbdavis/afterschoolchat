from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    # properties
    name = models.TextField()
    label = models.SlugField(unique=True)
    # owner = models.ForeignKey('auth.User', related_name='rooms')
    
    # relationships
    members = models.ManyToManyField(User)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    # properties
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    # relationships
    room = models.ForeignKey(Room, related_name='messages')
    
    # owner = models.ForeignKey('auth.User', related_name='messages')

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        # return self.timestamp.strftime('%b %-d %-I:%M %p')
        return self.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def as_dict(self):
        return {
            'id': self.id,
            'handle': self.handle,
            'message': self.message,
            'timestamp': self.formatted_timestamp,
            'room': self.room.id}
            