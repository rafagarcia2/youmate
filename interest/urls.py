from django.conf.urls import patterns, url

from interest import views

urlpatterns = patterns(
    '',
    url(regex=r'^interests/profile/$',
        view=views.UpdateProfileInterestsViews.as_view(),
        name='profile_interests'),
)
