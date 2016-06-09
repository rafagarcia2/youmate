from rest_framework import serializers
from chat.models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message