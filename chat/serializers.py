from rest_framework import serializers
from .models import Chat, Message

from django.conf import settings
from django.core.signing import TimestampSigner


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message

    def get_links(self, obj):
        signer = TimestampSigner(settings.WATERCOOLER_SECRET)
        channel = signer.sign(obj.pk)
        return {
            'channel': '{proto}://{server}/socket?channel={channel}'.format(
                proto='wss' if settings.TORNADOAPP_SECURE else 'ws',
                server=settings.TORNADOAPP_SERVER,
                channel=channel,
            ),
        }
