from django.conf.urls import patterns, url

from interest import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.InterestList.as_view(),
        name='interest_list'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.InterestUpdateView.as_view(),
        name='interest_detail'),
)
