from rest_framework import generics, status
from django.db.models import Q
from chat.models import Chat, Message
from chat import serializers
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

class ChatMixin(object):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer

class MessageMixin(object):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

class ChatList(ChatMixin, generics.ListCreateAPIView):
    '''View para visualizar todas as conversas do user.'''
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     raise NotAuthenticated()
        # from_user = self.request.user.profile
        from core.models import Profile
        from_user = Profile.objects.get(pk=4)

        queryset = super(ChatList, self).get_queryset()
        #queryset = self.queryset.filter(Q(from_user=from_user) | Q(to_user=from_user))

        return queryset

    def post(self, request, *args, **kwargs):
        # if not self.request.user.is_authenticated():
        #     raise NotAuthenticated()
        # from_user = self.request.user.profile

        # from core.models import Profile
        # from_user = Profile.objects.get(pk=3)

        from_user = self.request.query_params.get('from_user')
        to_user = self.request.query_params.get('to_user')
        queryset = Chat.objects.filter(Q(from_user=from_user, to_user=to_user) | Q(from_user=from_user, to_user=to_user))
        if queryset is not None: # if the chat already exist
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        return super(ChatList, self).post(request=request, *args, **kwargs)

class MessageView(MessageMixin, generics.ListCreateAPIView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     raise NotAuthenticated()
        # from_user = self.request.user.profile
        from core.models import Profile
        from_user = Profile.objects.get(pk=4)

        queryset = super(MessageView, self).get_queryset()
        to_chat = get_object_or_404(Chat, pk=self.kwargs.get('to_chat'))

        if not to_chat:
            return to_chat # Object Not found

        if to_chat.from_user != from_user and to_chat.to_user != from_user:
                return to_chat # Not found for the user

        queryset = self.queryset.filter(to_chat=to_chat)

        max_messages = self.request.query_params.get('max_messages', None)
        if max_messages is not None:
            queryset = self.queryset[:max_messages]

        return queryset

    def post(self, request, *args, **kwargs):
        # if not self.request.user.is_authenticated():
        #     raise NotAuthenticated()
        # from_user = self.request.user.profile
        from core.models import Profile
        from_user = Profile.objects.get(pk=4)
        to_chat = get_object_or_404(Chat, pk=self.kwargs.get('to_chat'))

        if  from_user not in [to_chat.from_user, to_chat.to_user]: # If the user is in chat
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        request.data.update(
            from_user=from_user.pk,
            to_chat = to_chat.pk
        )

        return super(MessageView, self).post(request=request, *args, **kwargs)