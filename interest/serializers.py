from rest_framework import serializers

from interest.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_image_url', read_only=True)
    slug = serializers.CharField(source='image_class', read_only=True)

    class Meta:
        model = Interest
        exclude = ('image_class',)


class FeedInterestSerializer(InterestSerializer):
    picture = serializers.CharField(source='get_image_url', read_only=True)
    name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Interest
        fields = ('id', 'picture', 'name')
