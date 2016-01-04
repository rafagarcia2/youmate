from django.contrib import auth
from django.db.models import Q

from rest_framework import generics, views, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from allauth.socialaccount.providers.facebook.views import (
    FacebookOAuth2Adapter)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from push_notifications.models import APNSDevice, GCMDevice

from api import serializers

from interest.models import Interest
from reference.models import Reference
from language.models import Language
from photo.models import Photo
from core.models import Profile
from mate.models import Mate


class APIRoot(views.APIView):
    def get(self, request):
        return Response({
            'YouMate': {
                'users': {
                    'users': reverse('user_list', request=request),
                    'logged_user': reverse(
                        'logged_user_retrieve', request=request),
                },
                'profile': {
                    'profiles': reverse('profile_list', request=request),
                    'mate': {
                        'pending_mates': reverse(
                            'profile_pending_mates', request=request),
                        'mates': reverse(
                            'profile_mates', request=request),
                        'add_mate': '/profiles/:pk/add_mate/',
                        'accept_mate': '/profiles/:pk/accept_mate/',
                        'reject_mate': '/profiles/:pk/reject_mate/',
                    }
                },
                'interests': reverse('interest_list', request=request),
                'references': reverse('reference_list', request=request),
                'languages': reverse('language_list', request=request),
                'photos': reverse('photo_list', request=request),
                'mates': reverse('mate_list', request=request),
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


class UserMixin(object):
    queryset = auth.get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class ProfileMixin(object):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class InterestMixin(object):
    queryset = Interest.objects.all()
    serializer_class = serializers.InterestSerializer


class MateMixin(object):
    queryset = Mate.objects.all()
    serializer_class = serializers.MateSerializer


class ReferenceMixin(object):
    queryset = Reference.objects.all()
    serializer_class = serializers.ReferenceSerializer


class LanguageMixin(object):
    queryset = Language.objects.all()
    serializer_class = serializers.LanguageSerializer


class PhotoMixin(object):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer


class APNSDeviceMixin(object):
    queryset = APNSDevice.objects.all()
    serializer_class = serializers.APNSDeviceSerializer


class GCMDeviceMixin(object):
    queryset = GCMDevice.objects.all()
    serializer_class = serializers.GCMDeviceSerializer


class UserList(UserMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'username': ['exact'],
        'first_name': ['icontains'],
        'last_name': ['icontains'],
        'profile__born_city': ['icontains'],
        'profile__living_city': ['icontains'],
        'profile__genre': ['icontains'],
        'profile__status': ['exact'],
    }

    def get_queryset(self):
        queryset = super(UserList, self).get_queryset()

        full_search = self.request.query_params.get('full_search', None)
        if full_search is not None:
            queryset = queryset.filter(
                Q(profile__living_city__icontains=full_search) |
                Q(first_name__icontains=full_search) |
                Q(last_name__icontains=full_search)
            )

        interests_ids = self.request.query_params.get(
            'profile__interests__id') or None
        try:
            interests_ids = interests_ids.split(',')
        except AttributeError:
            pass

        if isinstance(interests_ids, list):
            queryset = queryset.filter(
                profile__interests__id__in=interests_ids
            )
        return queryset


class UserRetrieve(UserMixin, generics.RetrieveUpdateAPIView):
    pass


class LoggedUserRetrieve(UserMixin, generics.RetrieveUpdateAPIView):
    def get_object(self):
        # from django.contrib.auth.models import User
        # return User.objects.get(username='admin')

        if self.request.user.is_authenticated():
            return self.request.user
        raise NotAuthenticated()

    def retrieve(self, request, pk=None):
        # from django.contrib.auth.models import User
        # return Response(serializers.UserSerializer(User.objects.get(username='admin')).data)

        if request.user.is_authenticated():
            return Response(serializers.UserSerializer(request.user).data)
        raise NotAuthenticated()


class InterestList(InterestMixin, generics.ListCreateAPIView):
    pass


class InterestUpdateView(InterestMixin, generics.RetrieveUpdateAPIView):
    pass


class MateList(MateMixin, generics.ListCreateAPIView):
    pass


class MateUpdateView(MateMixin, generics.RetrieveUpdateAPIView):
    pass


class ReferenceList(ReferenceMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'from_user', 'to_user')


class LanguageList(LanguageMixin, generics.ListCreateAPIView):
    pass


class PhotoList(PhotoMixin, generics.ListCreateAPIView):
    pass


class ProfileListView(ProfileMixin, generics.ListAPIView):
    def get_queryset(self):
        queryset = super(ProfileListView, self).get_queryset()

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(
                Q(living_city__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        return queryset


class ProfileUpdateView(ProfileMixin, generics.RetrieveUpdateAPIView):
    pass


class ProfileAddMateView(ProfileMixin, views.APIView):
    def post(self, request, format=None, pk=None):
        if self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()
        try:
            request.user.profile.add_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfilePendingMatesView(ProfileMixin, generics.RetrieveAPIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def retrieve(self, request, pk=None):
        serializer = serializers.ProfilePendingMatesSerializer(
            self.get_object()
        )
        return Response(serializer.data)


class ProfileMatesView(ProfileMixin, generics.RetrieveAPIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def retrieve(self, request, pk=None):
        serializer = serializers.ProfileMatesSerializer(
            self.get_object()
        )
        return Response(serializer.data)


class ProfileAcceptMateView(ProfileMixin, views.APIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def post(self, request, format=None, pk=None):
        self.object = self.get_object()
        try:
            request.user.profile.accept_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileRejectMateView(ProfileMixin, views.APIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def post(self, request, format=None, pk=None):
        self.object = self.get_object()
        try:
            request.user.profile.reject_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class APNSDeviceList(APNSDeviceMixin, generics.ListCreateAPIView):
    pass


class APNSDeviceRetrieve(APNSDeviceMixin, generics.RetrieveAPIView):
    pass


class GCMDeviceList(GCMDeviceMixin, generics.ListCreateAPIView):
    pass


class GCMDeviceRetrieve(GCMDeviceMixin, generics.RetrieveAPIView):
    pass
