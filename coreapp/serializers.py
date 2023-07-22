from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only = True)
    photo = serializers.ImageField(read_only = True)

    class Meta:
        model = UserProfile
        fields = "__all__"

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("photo",)
