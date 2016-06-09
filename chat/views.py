from rest_framework import generics

from chat.models import Chat, Message
from chat import serializers

from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from django.core.exceptions import ObjectDoesNotExist

class ChatMixin(object):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer

class MessageMixin(object):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

class ChatList(ChatMixin, generics.ListCreateAPIView):
    '''View para visualizar todas as conversas do user.'''
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile

        queryset = super(ChatList, self).get_queryset()
        queryset = self.queryset.filter(Q(from_user=from_user) | Q(to_user=from_user))

        return queryset

class MessageView(MessageMixin, generics.ListCreateAPIView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile

        queryset = super(MessageView, self).get_queryset()
        try:
            to_chat = Chat.objects.get(pk=self.kwargs.get('to_chat'))
        except ObjectDoesNotExist:
            return None

        # Testing user in chat
        if (to_chat.from_user != from_user and to_chat.to_user != from_user):
            return None

        queryset = self.queryset.filter(to_chat=to_chat)
        return queryset
