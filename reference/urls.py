from django.conf.urls import patterns, url

from reference import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.ReferenceList.as_view(),
        name='reference_list'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.ReferenceUpdateView.as_view(),
        name='reference_detail'),
)
