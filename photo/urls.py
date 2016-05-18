from django.conf.urls import patterns, url

from photo import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.PhotoList.as_view(),
        name='photo_list'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.PhotoRetrieveDelete.as_view(),
        name='photo_retrieve_delete'),
)
