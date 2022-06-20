from django.db import models
from django.contrib.auth.models import User
from user.models import UserFeedConf


class UserFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_conf = models.ForeignKey(UserFeedConf, on_delete=models.PROTECT)
    headline = models.CharField(max_length=355, null=True, blank=True)
    thumbnail = models.CharField(max_length=455, null=True, blank=True)
    source = models.CharField(max_length=455, null=True, blank=True)
    country = models.CharField(max_length=455, null=True, blank=True)
    detail_news = models.CharField(max_length=455, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


