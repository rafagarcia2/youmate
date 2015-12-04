from django.contrib import auth



from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from api import serializers

from interest.models import Interest
from core.models import Profile


class APIRoot(APIView):
    def get(self, request):
        return Response({
            'users': reverse('user_list', request=request),
            'interests': reverse('interest_list', request=request),
            'profiles': reverse('profile_list', request=request),
            'login': reverse('rest_login', request=request),
            'facebook_login': reverse('rest_facebook_login', request=request),
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


class UserList(UserMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'username': ['exact'],
        'first_name': ['icontains'],
        'last_name': ['icontains'],
        'profile__born_city': ['icontains'],
        'profile__living_city': ['icontains'],
    }


class UserRetrieve(UserMixin, generics.RetrieveAPIView):
    pass


class InterestList(InterestMixin, generics.ListCreateAPIView):
    pass


class ProfileListView(ProfileMixin, generics.ListAPIView):
    pass


class ProfileUpdateView(ProfileMixin, generics.RetrieveUpdateAPIView):
    pass


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
