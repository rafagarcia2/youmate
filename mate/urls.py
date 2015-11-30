from django.conf.urls import patterns, url

from mate import views

urlpatterns = patterns(
    '',
    url(regex=r'^become/mates/(?P<user__username>[\w-]+)/$',
        view=views.BecomeMatesView.as_view(),
        name='become-mates'),
    url(regex=r'^mates/(?P<username>[\w-]+)/$',
        view=views.MatesView.as_view(),
        name='mates'),
    url(regex=r'^mates/$',
        view=views.MatesView.as_view(),
        name='mates'),
)
