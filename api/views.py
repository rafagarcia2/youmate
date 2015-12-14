from django.contrib import auth
from django.db.models import Q

from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from rest_framework.filters import django_filters
from allauth.socialaccount.providers.facebook.views import (
    FacebookOAuth2Adapter)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from api import serializers

from interest.models import Interest
from reference.models import Reference
from language.models import Language
from core.models import Profile


class APIRoot(APIView):
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
                },
                'interests': reverse('interest_list', request=request),
                'references': reverse('reference_list', request=request),
                'languages': reverse('language_list', request=request),
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


class ReferenceMixin(object):
    queryset = Reference.objects.all()
    serializer_class = serializers.ReferenceSerializer


class LanguageMixin(object):
    queryset = Language.objects.all()
    serializer_class = serializers.LanguageSerializer


class UserList(UserMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'username': ['exact'],
        'first_name': ['icontains'],
        'last_name': ['icontains'],
        'profile__born_city': ['icontains'],
        'profile__living_city': ['icontains'],
        'profile__genre': ['icontains'],
        'profile__interests__title': ['icontains'],
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
        return queryset


class UserRetrieve(UserMixin, generics.RetrieveAPIView):
    pass


class LoggedUserRetrieve(UserMixin, generics.RetrieveAPIView):
    def retrieve(self, request, pk=None):
        if request.user.is_authenticated():
            return Response(serializers.UserSerializer(request.user).data)
        raise NotAuthenticated()


class InterestList(InterestMixin, generics.ListCreateAPIView):
    pass


class InterestUpdateView(InterestMixin, generics.RetrieveUpdateAPIView):
    pass


class ReferenceList(ReferenceMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'from_user', 'to_user')


class LanguageList(LanguageMixin, generics.ListCreateAPIView):
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


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
