from django.contrib import auth

from rest_framework import serializers

from core.models import Profile
from interest.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest


class ProfileSerializer(serializers.ModelSerializer):
    # interests = InterestSerializer(many=True)
    interests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Interest.objects.all()
    )

    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = auth.get_user_model()
