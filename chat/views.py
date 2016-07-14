import requests
from rest_framework import generics, status
from django.db.models import Q
from chat.models import Chat, Message
from chat import serializers
from django.shortcuts import get_object_or_404

from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ChatMixin(object):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatSerializer


class MessageMixin(object):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer


class UpdateHookMixin(object):
    """Classe Mixin para enviar atualizacoes ao servidor de websocket"""

    def _build_hook_url(self, pk):
        model = 'chat'
        return '{}://{}/{}/{}'.format(
            'https' if settings.TORNADOAPP_SECURE else 'http',
            settings.TORNADOAPP_SERVER, model, pk)

    def _send_hook_request(self, obj, method, pk):
        url = self._build_hook_url(pk)
        if method in ('POST', 'PUT'):
            serializer = self.get_serializer(obj)
            renderer = JSONRenderer()
            context = {'request': self.request}
            body = renderer.render(
                serializer.data,
                renderer_context=context)
        else:
            body = None
        headers = {
            'content-type': 'application/json',
        }
        try:
            response = requests.request(method, url,
                data=body, timeout=0.5, headers=headers)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            # Host nao pode ser resolvido ou conexao foi recusada
            pass
        except requests.exceptions.Timeout:
            # Solicitacao expirou
            pass
        except requests.exceptions.RequestException:
            # Servidor respondeu com codigo 4XX ou 5XX
            pass

    def perform_create(self, serializer):
        #super(MessageView, self).perform_create(serializer)
        from .models import Chat
        chat = Chat.objects.get(pk=serializer.data['to_chat'])
        f_user = serializer.data['from_user']
        channel = chat.from_user if chat.from_user != f_user else chat.to_user
        self._send_hook_request(serializer.instance, 'POST', channel.pk)


class ChatList(ChatMixin, generics.ListCreateAPIView):
    '''View para visualizar todas as conversas do user.'''
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile

        queryset = super(ChatList, self).get_queryset()
        queryset = queryset.filter(Q(from_user=from_user) | Q(to_user=from_user))

        return queryset


class MessageView(MessageMixin, UpdateHookMixin, generics.ListCreateAPIView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile

        queryset = super(MessageView, self).get_queryset()
        to_chat = get_object_or_404(Chat, pk=self.kwargs.get('to_chat'))

        if not to_chat:
            return to_chat # Object Not found

        if to_chat.from_user != from_user and to_chat.to_user != from_user:
                return to_chat # Not found for the user

        queryset = self.queryset.filter(to_chat=to_chat)

        top_messages = self.request.query_params.get('top_messages', None)
        bottom_messages = self.request.query_params.get('bottom_messages', None)
        if top_messages != None and bottom_messages != None:
            queryset = queryset[top_messages:bottom_messages]

        return queryset

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        from_user = self.request.user.profile
        to_chat = get_object_or_404(Chat, pk=self.kwargs.get('to_chat'))

        if from_user not in [to_chat.from_user, to_chat.to_user]: # If the user in chat
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        request.data.update(
            from_user=from_user.pk,
            to_chat=to_chat.pk
        )
        return super(MessageView, self).post(request=request, *args, **kwargs)
