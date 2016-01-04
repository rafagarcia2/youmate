from django.contrib import auth

from rest_framework import serializers
from push_notifications.models import APNSDevice, GCMDevice

from core.models import Profile
from interest.models import Interest
from reference.models import Reference
from language.models import Language
from photo.models import Photo
from mate.models import Mate


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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


class ValidateProfilersCount(object):
    def __init__(self):
        self.max = 7

    def __call__(self, instance):
        if instance.photos.count() > self.max:
            message = ('You cannot have more than %s photos.' % (self.max))
            raise serializers.ValidationError(message)


class PhotoUrlSerializer(serializers.ModelSerializer):
    image = serializers.CharField(
        source='get_photo_url',
        read_only=True
    )

    class Meta:
        model = Photo
        fields = ('image',)


class PhotoSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(),
        validators=[ValidateProfilersCount()]
    )
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Photo


class MateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mate


class ValidateInterestsCount(object):
    def __init__(self):
        self.min = 1
        self.max = 4

    def __call__(self, data):
        interests = data.get('interests', [])
        if not (self.min <= len(interests) <= self.max):
            message = ('You cannot have more than %s interests.' % self.max)
            raise serializers.ValidationError(message)


class ProfileSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True)
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
    # photos = PhotoUrlSerializer(many=True, read_only=True)
    photos = serializers.ListField(
        source='get_photos',
        read_only=True
    )
    photo = Base64ImageField(
        max_length=None, use_url=True,
    )
    mates = serializers.PrimaryKeyRelatedField(
        source='mates_profiles',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Profile
        validators = [
            ValidateInterestsCount()
        ]

    def update(self, instance, validated_data):
        try:
            instance.interests = validated_data.pop('interests')
        except KeyError:
            pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProfileMateActionsSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(),
        validators=[ValidateProfilersCount()]
    )

    class Meta:
        model = Profile
        fields = ('profile',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = auth.get_user_model()
        exclude = ('password',)


class ProfilePendingMatesSerializer(serializers.ModelSerializer):
    mates = UserSerializer(
        source='peding_mates_user',
        many=True,
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ('mates',)


class ProfileMatesSerializer(serializers.ModelSerializer):
    mates = ProfileSerializer(
        source='mates_profiles',
        many=True,
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ('mates',)


class APNSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = APNSDevice


class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
