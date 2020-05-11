import uuid
from datetime import datetime
from time import timezone
from typing import Any

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

def upload_to_user(instance, filename):
    return '{0}/zinnour_{1}_{2}'.format('scripts', instance.date_created_on_ms, filename)


class TrainingSession(models.Model):
    session_name = models.CharField(max_length=200, default='')
    batch_size = models.IntegerField(default=64)
    epochs = models.IntegerField(default=10)
    optimizer = models.CharField(max_length=100, default='')
    loss = models.CharField(max_length=100, default='')
    metrics = models.CharField(max_length=50, default='')
    state = models.BooleanField()
    type = models.CharField(max_length=50, default='')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    script = models.FileField(upload_to=upload_to_user, default='')
    searcher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def date_created_on_ms(self):
        return int(self.date_created.timestamp())
