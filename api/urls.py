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

    # Push notification
    url(regex=r'^device/apns/',
        view=views.APNSDeviceList.as_view(),
        name='device_apns_list'),
    url(regex=r'^device/apns/(?P<pk>[0-9]+)/$',
        view=views.APNSDeviceRetrieve.as_view(),
        name='device_apns_retrieve'),
    url(regex=r'^device/gcm/',
        view=views.GCMDeviceList.as_view(),
        name='device_gcm_list'),
    url(regex=r'^device/gcm/(?P<pk>[0-9]+)/$',
        view=views.GCMDeviceRetrieve.as_view(),
        name='device_gcm_retrieve'),

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

    # Api urls
    url(r'^photos/', include('photo.urls')),
    url(r'^polls/', include('poll.urls')),
    url(r'^interests/', include('interest.urls')),
    url(r'^mates/', include('mate.urls')),
    url(r'^languages/', include('language.urls')),
    url(r'^references/', include('reference.urls')),
)
