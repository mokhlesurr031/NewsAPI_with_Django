from rest_framework import serializers
from .models import UserFeed


class UserFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeed
        fields = '__all__'