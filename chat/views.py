from rest_framework import generics

from chat.models import Chat
from chat import serializers

# Teste Inicial, nada fixo ainda, tudo pode ser substituido.

class ChatMixin(object):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer


class ChatList(ChatMixin, generics.ListCreateAPIView):
    '''View para visualizar todas as conversas do user.'''
    def get_queryset(self):
        queryset = super(ChatList, self).get_queryset()
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile

        queryset = self.queryset.filter(from_user=from_user) | self.queryset.filter(to_user=from_user)
        return queryset

class ChatView(ChatMixin, generics.ListCreateAPIView):
    '''View para visualizar cada conversa em particular.'''
    def get_queryset(self):
        queryset = super(ChatList, self).get_queryset()
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile

        to_user = Profile.objects.get(pk=self.kwargs.get('to_user'))
        queryset = self.queryset.filter(from_user=from_user, to_user=to_user) | self.queryset.filter(from_user=to_user, to_user=from_user)

        return queryset