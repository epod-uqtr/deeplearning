from datetime import datetime
from time import timezone
from typing import Any

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

def upload_to_user(instance, filename):
    return '{0}/zinnour_{1}_{2}'.format('scripts', instance.date_created_on_ms, filename)


class TrainingSession(models.Model):
    state = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    script = models.FileField(upload_to=upload_to_user)
    searcher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def date_created_on_ms(self):
        return int(self.date_created.timestamp())