from django.conf.urls import patterns, url
from rest_framework import generics, views, status
from chat import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.ChatList.as_view(),
        name='chat_list'),
)
