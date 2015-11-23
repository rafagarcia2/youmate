from django.conf.urls import patterns, url

from reference import views

urlpatterns = patterns(
    '',
    url(regex=r'^references/add/$',
        view=views.ReferenceCreateView.as_view(),
        name='add_reference'),
    url(regex=r'^references/(?P<id>\d+)/active/$',
        view=views.ReferenceActiveView.as_view(),
        name='active_reference'),
)
