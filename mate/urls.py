from django.conf.urls import patterns, url

from mate import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.MateList.as_view(),
        name='mate_list'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.MateUpdateView.as_view(),
        name='mate_detail'),
)
