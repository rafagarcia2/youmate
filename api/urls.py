from django.conf.urls import patterns, url, include

from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework.routers import DefaultRouter

# from push_notifications.api.rest_framework import (
#     APNSDeviceAuthorizedViewSet,
#     GCMDeviceAuthorizedViewSet
# )

# Class based API views
from api import views

# router = DefaultRouter()
# router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
# router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)

urlpatterns = patterns(
    '',
    # Root
    url(regex=r'^$',
        view=views.APIRoot.as_view(),
        name='root'),

    # Push notification
    # url(r'^device/apns/', APNSDeviceAuthorizedViewSet.as_view(), name='device_apns'),
    # url(r'^device/gcm/', GCMDeviceAuthorizedViewSet, name='device_gcm'),
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

    # User
    url(regex=r'^users/feed/$',
        view=views.UserFeedList.as_view(),
        name='user_feed_list'),
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
    url(regex=r'^profiles/logout/$',
        view=views.ProfileLogoutView.as_view(),
        name='profile_logout'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/$',
        view=views.ProfileUpdateView.as_view(),
        name='profile_detail'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/add_mate/$',
        view=views.ProfileAddMateView.as_view(),
        name='profile_add_mate'),
    url(regex=r'^profiles/pending_mates/$',
        view=views.ProfilePendingMatesView.as_view(),
        name='profile_pending_mates'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/accept_mate/$',
        view=views.ProfileAcceptMateView.as_view(),
        name='profile_accept_mate'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/reject_mate/$',
        view=views.ProfileRejectMateView.as_view(),
        name='profile_reject_mate'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/delete_mate/$',
        view=views.ProfileDeleteMateView.as_view(),
        name='profile_delete_mate'),
    url(regex=r'^profiles/(?P<pk>[0-9]+)/cancel_mate/$',
        view=views.ProfileCancelMateView.as_view(),
        name='profile_cancel_mate'),
    url(regex=r'^profiles/mates/$',
        view=views.ProfileMatesView.as_view(),
        name='profile_mates'),
    url(regex=r'^profiles/reset_email_code/$',
        view=views.ProfileResetEmailCodeView.as_view(),
        name='profile_reset_email_code'),
    url(regex=r'^profiles/reset_phone_code/$',
        view=views.ProfileResetPhoneCodeView.as_view(),
        name='profile_reset_phone_code'),
    url(regex=r'^profiles/confirm_phone_code/$',
        view=views.ProfileConfirmPhoneCodeView.as_view(),
        name='profile_confirm_phone_code'),
    url(regex=r'^profiles/polls/$',
        view=views.ProfilePollsView.as_view(),
        name='profile_polls'),

    # Interest
    url(regex=r'^interests/$',
        view=views.InterestList.as_view(),
        name='interest_list'),
    url(regex=r'^interests/(?P<pk>[0-9]+)/$',
        view=views.InterestUpdateView.as_view(),
        name='interest_detail'),

    # Reference
    url(regex=r'^references/$',
        view=views.ReferenceList.as_view(),
        name='reference_list'),
    url(regex=r'^references/(?P<pk>[0-9]+)/$',
        view=views.ReferenceUpdateView.as_view(),
        name='reference_detail'),

    # Language
    url(regex=r'^languages/$',
        view=views.LanguageList.as_view(),
        name='language_list'),

    # Photo
    url(regex=r'^photos/$',
        view=views.PhotoList.as_view(),
        name='photo_list'),
    url(regex=r'^photos/(?P<pk>[0-9]+)/$',
        view=views.PhotoRetrieveDelete.as_view(),
        name='photo_retrieve_delete'),

    # Mate
    url(regex=r'^mates/$',
        view=views.MateList.as_view(),
        name='mate_list'),
    url(regex=r'^mates/(?P<pk>[0-9]+)/$',
        view=views.MateUpdateView.as_view(),
        name='mate_detail'),

    # Poll
    url(regex=r'^polls/$',
        view=views.PollList.as_view(),
        name='poll_list'),
    url(regex=r'^polls/create/$',
        view=views.PollCreateView.as_view(),
        name='poll_create'),
    url(regex=r'^polls/(?P<pk>[0-9]+)/$',
        view=views.PollDetailView.as_view(),
        name='poll_detail'),
    url(regex=r'^polls/(?P<pk>[0-9]+)/update/$',
        view=views.PollUpdateView.as_view(),
        name='poll_update'),
    url(regex=r'^polls/(?P<poll__pk>[0-9]+)/answers/$',
        view=views.AnswerList.as_view(),
        name='poll_list'),
    url(regex=r'^polls/(?P<poll__pk>[0-9]+)/answers/(?P<pk>[0-9]+)/$',
        view=views.AnswerUpdateView.as_view(),
        name='poll_detail'),
    url(regex=r'^polls/(?P<poll__pk>[0-9]+)/answers/(?P<pk>[0-9]+)/like/$',
        view=views.AnswerLikeView.as_view(),
        name='poll_like'),
    url(regex=r'^polls/(?P<poll__pk>[0-9]+)/answers/(?P<pk>[0-9]+)/deslike/$',
        view=views.AnswerDeslikeView.as_view(),
        name='poll_deslike'),
)
