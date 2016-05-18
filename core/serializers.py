from django.contrib import auth

from rest_framework import serializers, pagination

from core.models import Profile
from interest.models import Interest
from reference.models import Reference

from language.serializers import LanguageSerializer
from interest.serializers import FeedInterestSerializer

from api.validators import ValidateInterestsCount, ValidateProfilersCount
from api.serializers import Base64ImageField


class ProfileSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(
        many=True,
        read_only=True,
    )
    interests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Interest.objects.all(),
        validators=[ValidateInterestsCount()]
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
    photo_url = serializers.CharField(
        source='get_photo_url',
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
    interests = FeedInterestSerializer(many=True, read_only=True)
    referece = serializers.DictField(
        source='get_pretty_referece',
        read_only=True
    )
    photo_url = serializers.CharField(
        source='get_photo_url',
        read_only=True
    )

    class Meta:
        model = Profile
        validators = [
            ValidateInterestsCount()
        ]
        fields = (
            'id', 'photo_url', 'age', 'living_city',
            'interests', 'referece', 'status',
        )


class UserFeedSerializer(UserSerializer):
    profile = ProfileFeedSerializer()

    class Meta:
        model = auth.get_user_model()
        fields = (
            'id', 'first_name', 'last_name', 'profile'
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


class PollProfileSerializer(ProfileFeedSerializer):
    picture = serializers.CharField(
        source='get_photo_url',
        read_only=True
    )
    full_name = serializers.CharField(
        source='user.get_full_name', read_only=True)

    class Meta:
        model = Profile
        validators = [
            ValidateInterestsCount()
        ]
        fields = (
            'id', 'picture', 'living_city', 'full_name',
        )
