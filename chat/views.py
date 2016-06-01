from rest_framework import generics

from chat.models import Chat
from chat import serializers

# Teste Inicial, nada fixo ainda, tudo pode ser substituido.

class ChatMixin(object):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer


class ChatList(ChatMixin, generics.ListCreateAPIView):
    pass
