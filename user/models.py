from django.db import models
from django.contrib.auth.models import User


class UserFeedConf(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    countries = models.CharField(max_length=355)
    sources = models.CharField(max_length=355)
    keywords = models.CharField(max_length=355)