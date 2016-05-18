from rest_framework import serializers

from photo.models import Photo
from core.models import Profile
from api.serializers import Base64ImageField
from api.validators import ValidateProfilersCount


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
