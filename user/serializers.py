from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserFeedConf


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserFeedConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedConf
        fields = '__all__'