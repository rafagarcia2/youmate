from django.contrib import auth

from rest_framework import serializers
from push_notifications.models import APNSDevice, GCMDevice

from core.models import Profile
from interest.models import Interest
from reference.models import Reference
from language.models import Language


class InterestSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_image_url', read_only=True)
    slug = serializers.CharField(source='image_class', read_only=True)

    class Meta:
        model = Interest
        exclude = ('image_class',)


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language


class ValidateInterestsCount(object):
    def __init__(self):
        self.min = 1
        self.max = 4

    def __call__(self, data):
        interests = data.get('interests', [])
        if not (self.min <= len(interests) <= self.max):
            message = ('You cannot have less than %s '
                       'and no more than %s interests.' % (self.min, self.max))
            raise serializers.ValidationError(message)


class ProfileSerializer(serializers.ModelSerializer):
    # interests = InterestSerializer(many=True)
    interests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Interest.objects.all(),
        validators=[ValidateInterestsCount()]
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
        validators = [
            ValidateInterestsCount()
        ]


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
