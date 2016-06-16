from django.conf.urls import url

from mate import views

urlpatterns = [
    url(regex=r'^$',
        view=views.MateList.as_view(),
        name='mate_list'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.MateUpdateView.as_view(),
        name='mate_detail'),
]
