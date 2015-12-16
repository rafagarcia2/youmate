from django.contrib import auth

from rest_framework import serializers
from push_notifications.models import APNSDevice, GCMDevice

from core.models import Profile
from interest.models import Interest
from reference.models import Reference


class InterestSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_image_url', read_only=True)
    slug = serializers.CharField(source='image_class', read_only=True)

    class Meta:
        model = Interest
        exclude = ('image_class',)


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference


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
    references = serializers.PrimaryKeyRelatedField(
        source='references_to',
        many=True,
        queryset=Reference.objects.all()
    )
    reference_rate = serializers.CharField(
        source='get_average_rate',
        read_only=True
    )

    class Meta:
        model = Profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = auth.get_user_model()
        exclude = ('password',)


class APNSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = APNSDevice


class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
