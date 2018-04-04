from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Urls(models.Model):
    url = models.URLField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add = True)
    visits = models.IntegerField(default=0)
