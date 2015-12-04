from django.conf.urls import patterns, url, include

# Class based API views
from api import views

urlpatterns = patterns(
    '',
    # Root
    url(regex=r'^$',
        view=views.APIRoot.as_view(),
        name='root'),

    # Authentication
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/',
        include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$',
        views.FacebookLogin.as_view(), name='rest_facebook_login'),

    # User
    url(regex=r'^users/$',
        view=views.UserList.as_view(),
        name='user_list'),
    url(regex=r'^users/(?P<pk>[0-9]+)/$',
        view=views.UserRetrieve.as_view(),
        name='user_retrieve'),

    # Profile
    url(regex=r'^profiles/$',
        view=views.ProfileListView.as_view(),
        name='profile_list'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/$',
        view=views.ProfileUpdateView.as_view(),
        name='profile_detail'),

    # Interest
    url(regex=r'^interests/$',
        view=views.InterestList.as_view(),
        name='interest_list'),
)
