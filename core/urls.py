from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'),
    url(regex=r'profile/$',
        view=views.ProfileView.as_view(),
        name='profile'),
    url(regex=r'profile/update/$',
        view=views.UpdateProfileView.as_view(),
        name='update_profile'),
    url(regex=r'profiles/search/$',
        view=views.SearchProfileView.as_view(),
        name='search_profile'),
)
