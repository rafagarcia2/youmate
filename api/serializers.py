from django.contrib import auth

from rest_framework import serializers, pagination
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
    from_user__photo_url = serializers.CharField(
        source='from_user.get_photo_url', read_only=True)
    from_user__pk = serializers.CharField(
        source='from_user.user.pk', read_only=True)
    from_user__first_name = serializers.CharField(
        source='from_user.user.first_name', read_only=True)
    from_user__last_name = serializers.CharField(
        source='from_user.user.last_name', read_only=True)
    to_user__pk = serializers.CharField(
        source='to_user.user.pk', read_only=True)

    class Meta:
        model = Reference

    def validate_users_are_mate(self, data):
        from_user = data.get('from_user')
        to_user = data.get('to_user')
        if not from_user.mates_users.filter(profile=to_user).exists():
            message = ('You can only create references for your mates.')
            raise serializers.ValidationError(message)

    def validate(self, data):
        self.validate_users_are_mate(data=data)
        return super(ReferenceSerializer, self).validate(data)


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
    photos = serializers.ListField(
        source='get_photos',
        read_only=True
    )
    photo = Base64ImageField(
        max_length=None, use_url=True,
    )
    device_registration_ids = serializers.ListField(
        source='get_device_registration_ids',
        read_only=True,
    )

    class Meta:
        model = Profile
        exclude = ('mates', 'email_code', 'phone_code',)
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
    full_name = serializers.CharField(
        source='get_full_name', read_only=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        model = auth.get_user_model()
        exclude = (
            'password', 'last_login', 'is_superuser',
            'is_staff', 'is_active', 'date_joined', 'groups',
            'user_permissions',
        )


class ProfileFeedSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        validators = [
            ValidateInterestsCount()
        ]
        fields = (
            'id', 'photo_url', 'age', 'living_city',
            'interests', 'references',
        )


class UserFeedSerializer(UserSerializer):
    profile = ProfileFeedSerializer()

    class Meta:
        model = auth.get_user_model()
        fields = (
            'id', 'full_name', 'profile'
        )


class PaginatedUserSerializer(pagination.PageNumberPagination):
    # page_size = 20
    page_size = 2

    class Meta:
        object_serializer_class = UserSerializer


class ProfilePendingMatesSerializer(serializers.ModelSerializer):
    mates = UserSerializer(
        source='peding_mates_users',
        many=True,
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ('mates',)


class ProfileMatesSerializer(serializers.ModelSerializer):
    mates = UserSerializer(
        source='mates_users',
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
