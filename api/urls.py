from django.conf.urls import patterns, url, include

from rest_framework.authtoken.views import obtain_auth_token

# Class based API views
from api import views

urlpatterns = patterns(
    '',
    # Root
    url(regex=r'^$',
        view=views.APIRoot.as_view(),
        name='root'),

    # Authentication
    url(r'^rest-social-auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^oauth2/',
        include('oauth2_provider.urls', namespace='oauth2')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/get-token/',
        view=obtain_auth_token,
        name='rest_obtain_token'),
    url(r'^rest-auth/registration/',
        include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$',
        views.FacebookLogin.as_view(), name='rest_facebook_login'),
    url(r'^rest-auth/google/$',
        views.GoogleLogin.as_view(), name='rest_google_login'),

    # User
    url(regex=r'^users/$',
        view=views.UserList.as_view(),
        name='user_list'),
    url(regex=r'^users/(?P<pk>[0-9]+)/$',
        view=views.UserRetrieve.as_view(),
        name='user_retrieve'),
    url(regex=r'^users/logged_user/$',
        view=views.LoggedUserRetrieve.as_view(),
        name='logged_user_retrieve'),

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
    url(regex=r'^interests/(?P<pk>[0-9]+)/$',
        view=views.ProfileUpdateView.as_view(),
        name='interest_detail'),

    # Reference
    url(regex=r'^references/$',
        view=views.ReferenceList.as_view(),
        name='reference_list'),
)
