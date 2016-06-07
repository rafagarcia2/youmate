from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.reverse import reverse

from allauth.socialaccount.providers.facebook.views import (
    FacebookOAuth2Adapter)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from api import mixins


class APIRoot(views.APIView):
    def get(self, request):
        return Response({
            'YouMate': {
                'users': {
                    'users': reverse('user_list', request=request),
                    'users_feed': reverse('user_feed_list', request=request),
                    'logged_user': reverse(
                        'logged_user_retrieve', request=request),
                },
                'profile': {
                    'profiles': reverse('profile_list', request=request),
                    'mate': {
                        'logout': reverse(
                            'profile_logout', request=request),
                        'pending_mates': reverse(
                            'profile_pending_mates', request=request),
                        'mates': reverse(
                            'profile_mates', request=request),
                        'polls': reverse(
                            'profile_polls', request=request),
                        'add_mate': '/profiles/:pk/add_mate/',
                        'cancel_mate': '/profiles/:pk/cancel_mate/',
                        'accept_mate': '/profiles/:pk/accept_mate/',
                        'reject_mate': '/profiles/:pk/reject_mate/',
                        'delete_mate': '/profiles/:pk/delete_mate/',
                        'reset_email_code': reverse(
                            'profile_reset_email_code', request=request),
                        'reset_phone_code': reverse(
                            'profile_reset_phone_code', request=request),
                        'confirm_phone_code': reverse(
                            'profile_confirm_phone_code', request=request),
                    }
                },
                'interests': reverse('interest_list', request=request),
                'references': reverse('reference_list', request=request),
                'languages': reverse('language_list', request=request),
                'photos': reverse('photo_list', request=request),
                'mates': reverse('mate_list', request=request),
                'references': reverse('reference_list', request=request),
                'chat': reverse('chat_list', request=request),
                'polls': {
                    'polls': reverse('poll_list', request=request),
                    'polls_create': reverse('poll_create', request=request),
                    'polls_detail': '/polls/:pk/',
                    'polls_update': '/polls/:pk/update/',
                    'answers': {
                        'answers': '/polls/:pk/answers/',
                        'answers_create': '/polls/:pk/answers/create/',
                        'answers_like': 'polls/:pk/answers/:pk/like/',
                        'answers_deslike': 'polls/:pk/answers/:pk/deslike/',
                    },
                },
            },
            'Oauth2': {
                'oauth2_authorize': reverse(
                    'oauth2:authorize', request=request),
                'oauth2_token': reverse('oauth2:token', request=request),
                'oauth2_revoke-token': reverse(
                    'oauth2:revoke-token', request=request),
            },
            'Authentication': {
                'obtain_token': reverse('rest_obtain_token', request=request),
                'login': reverse('rest_login', request=request),
                'facebook_login': reverse(
                    'rest_facebook_login', request=request),
                'google_login': reverse('rest_google_login', request=request),
            },
            'Devices': {
                'device_apns': reverse('device_apns_list', request=request),
                'device_gcm': reverse('device_gcm_list', request=request),
            }
        })


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class APNSDeviceList(mixins.APNSDeviceMixin, generics.ListCreateAPIView):
    pass


class APNSDeviceRetrieve(mixins.APNSDeviceMixin, generics.RetrieveAPIView):
    pass


class GCMDeviceList(mixins.GCMDeviceMixin, generics.ListCreateAPIView):
    pass


class GCMDeviceRetrieve(mixins.GCMDeviceMixin, generics.RetrieveAPIView):
    pass
