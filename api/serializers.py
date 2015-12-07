from django.contrib import auth

from rest_framework import serializers

from core.models import Profile
from interest.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_image_url', read_only=True)
    slug = serializers.CharField(source='image_class', read_only=True)

    class Meta:
        model = Interest
        exclude = ('image_class',)


class ProfileSerializer(serializers.ModelSerializer):
    # interests = InterestSerializer(many=True)
    interests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Interest.objects.all()
    )
    photo_url = serializers.CharField(
        source='get_photo_url',
        read_only=True
    )

    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = auth.get_user_model()
