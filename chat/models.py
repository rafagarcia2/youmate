from __future__ import unicode_literals

from django.db import models
from django_extensions.db.fields import CreationDateTimeField

class Chat(models.Model):
    text = models.CharField('mensagem', max_length=400)
    pub_date = CreationDateTimeField() # Verificar com datetime
    from_user = models.ForeignKey(to='core.Profile', related_name='chats_from')
    to_user = models.ForeignKey(to='core.Profile', related_name='chats_to')

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

    # def get_chat(self): # Peguar minha conversas
    #     return self.chat.filter(
    #         to_user__from_user=self)

    # def get_chat_with_me(self): 
    #     return self.chat_with_me.filter(
    #         from_user__to_user=self)