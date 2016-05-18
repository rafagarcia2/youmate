from rest_framework import serializers

from mate.models import Mate


class MateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mate
