from django.db.models import Q, Avg
from django.db.models.functions import Coalesce
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib import auth

from vanilla import TemplateView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, views, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework import filters
from geopy.geocoders import Nominatim

from core.forms import UpdateProfileAboutForm, ValidatePhoneForm
from reference.forms import ReferenceForm
from core.models import Profile, code_generate
from core import serializers


class UserMixin(object):
    queryset = auth.get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class UserFeedMixin(UserMixin):
    serializer_class = serializers.UserFeedSerializer


class ProfileMixin(object):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class IndexView(TemplateView):
    template_name = 'index.html'


class ProfileView(DetailView):
    model = Profile
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update(reference_form=ReferenceForm())
        context.update(
            update_profile_about_form=UpdateProfileAboutForm(
                instance=self.get_object()))
        return context

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs.get('username')

        if not username and self.request.user.is_authenticated():
            return self.request.user.profile
        else:
            return get_object_or_404(queryset, user__username=username)


class ValidatePhoneView(DetailView):
    model = Profile
    template_name = 'account/profile/validate_phone.html'

    def get_context_data(self, **kwargs):
        context = super(ValidatePhoneView, self).get_context_data(**kwargs)
        context.update(validate_phone_form=ValidatePhoneForm())
        return context

    def get_object(self):
        return self.request.user.profile


class ConfirmationEmail(DetailView):
    model = Profile
    template_name = 'account/confirmation_email_verified.html'

    def get_object(self):
        queryset = self.get_queryset()
        email_code = self.kwargs.get('email_code')
        try:
            profile = get_object_or_404(queryset, email_code=email_code)
        except:
            profile = None
        else:
            profile.is_email_verified = True
            profile.email_code = code_generate(size=32)
            profile.save()
        return profile


class ConfirmationPhone(APIView):
    queryset = Profile.objects.all()

    def put(self, request, **kwargs):
        self.object = self.get_object()

        self.object.is_phone_verified = True
        self.object.save()

        return Response({
            'profile_id': self.object.id,
            'is_phone_verified': self.object.is_phone_verified,
        })

    def get_object(self):
        phone_code = self.kwargs.get('phone_code')
        profile = get_object_or_404(self.queryset, phone_code=phone_code)
        profile.is_phone_verified = True
        profile.phone_code = code_generate()
        profile.save()
        return profile


class UserList(UserMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = serializers.PaginatedUserSerializer
    filter_fields = {
        # custom_filters: [
        #     'latitude', 'longitude', 'address',
        #     'full_search', 'profile__interests__id',
        # ]
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
        latitude = self.request.query_params.get(
            'latitude') or None
        longitude = self.request.query_params.get(
            'longitude') or None
        address = self.request.query_params.get(
            'address') or None

        if address:
            geolocator = Nominatim()
            location = geolocator.geocode(address)
            try:
                latitude, longitude = location.point[:-1]
            except:
                location = geolocator.geocode(address.split('-')[0])
                try:
                    latitude, longitude = location.point[:-1]
                except:
                    pass
            else:
                latitude, longitude = location.point[:-1]

        if latitude and longitude:
            query = """
                SELECT
                  query.id
                FROM (
                    SELECT id, (6371 *
                        acos(
                            cos(radians(%(latitude)s)) *
                            cos(radians(latitude)) *
                            cos(radians(%(longitude)s) - radians(longitude)) +
                            sin(radians(%(latitude)s)) *
                            sin(radians(latitude))
                        )
                    ) distance
                    FROM core_coreuser
                    GROUP BY id
                ) query
                WHERE distance <= %(distance)s;
            """ % {
                'latitude': latitude,
                'longitude': longitude,
                'distance': 100,
            }

            cursor = connection.cursor()
            cursor.execute(query)
            ids = [i[0] for i in cursor.fetchall()]
            queryset = queryset.filter(id__in=ids)

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

        if self.request.user.is_authenticated():
            queryset = queryset.exclude(pk=self.request.user.pk)

        queryset = queryset.annotate(
            rating=Coalesce(Avg('profile__references_to__rating'), 0)
        ).order_by('-rating')

        queryset = queryset.distinct()
        return queryset


class UserFeedList(UserList, UserFeedMixin):
    pass


class UserRetrieve(UserMixin, generics.RetrieveUpdateAPIView):
    def get(self, *args, **kwargs):
        response = super(UserRetrieve, self).get(*args, **kwargs)
        if not self.request.user.is_authenticated():
            return response

        instance = self.get_object()
        if self.request.user.pk != kwargs.get('pk'):
            mate_status = self.request.user.profile.get_mate_status(
                instance.profile)
            response.data['profile'].update(mate_status=mate_status)

        return response

    def patch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()

        language_ids = self.request.data.get('profile__language_ids')
        try:
            language_ids = language_ids.split(',')
        except AttributeError:
            pass
        else:
            self.object.profile.update_languages(language_ids)

        return super(UserRetrieve, self).patch(
            request, *args, **kwargs)


class LoggedUserRetrieve(UserMixin, generics.RetrieveUpdateAPIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user
        raise NotAuthenticated()

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated():
            return Response(serializers.UserSerializer(request.user).data)
        raise NotAuthenticated()


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
    def get(self, *args, **kwargs):
        response = super(ProfileUpdateView, self).get(*args, **kwargs)
        if not self.request.user.is_authenticated():
            return response

        instance = self.get_object()
        if self.request.user.pk != kwargs.get('pk'):
            mate_status = self.request.user.profile.get_mate_status(instance)
            response.data.update(mate_status=mate_status)

        return response

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.request.user.is_authenticated() and \
           self.request.user.profile != self.object:
            raise NotAuthenticated()

        language_ids = self.request.data.get('language_ids')
        try:
            language_ids = language_ids.split(',')
        except AttributeError:
            pass
        else:
            self.object.update_languages(language_ids)

        return super(ProfileUpdateView, self).patch(
            request, *args, **kwargs)


class ProfileAddMateView(ProfileMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def post(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        profile = self.request.user.profile
        self.object = self.get_object()

        # Mates of any kind
        already_mates = profile.all_mates.filter(
            Q(to_user=self.object) | Q(from_user=self.object)
        ).exists()

        if already_mates:
            message = ('You can only ask for mate once.')
            return Response(
                {'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile.add_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAcceptMateView(ProfileMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def post(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()
        try:
            request.user.profile.accept_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileRejectMateView(ProfileMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def post(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()
        try:
            request.user.profile.reject_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDeleteMateView(ProfileMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def delete(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()
        try:
            self.request.user.profile.delete_mate(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileLogoutView(ProfileMixin, views.APIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def post(self, request, format=None, pk=None):
        self.object = self.get_object()
        device_id = self.request.data.get('device_id', None)

        try:
            self.object.logout(device_id)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileCancelMateView(ProfileMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def delete(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()
        try:
            self.request.user.profile.cancel_mate(self.object)
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


class ProfilePollsView(ProfileMixin, generics.RetrieveAPIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def retrieve(self, request, pk=None):
        serializer = serializers.ProfilePollsSerializer(
            self.get_object()
        )
        return Response(serializer.data)


class ProfileResetEmailCodeView(ProfileMixin, views.APIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def post(self, request, format=None, pk=None):
        self.object = self.get_object()
        try:
            self.object.send_email_verification(reset_email=True)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_200_OK)


class ProfileResetPhoneCodeView(ProfileMixin, views.APIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def post(self, request, format=None, pk=None):
        self.object = self.get_object()
        try:
            self.object.send_phone_verification(reset_phone=True)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_200_OK)


class ProfileConfirmPhoneCodeView(ProfileMixin, views.APIView):
    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile
        raise NotAuthenticated()

    def post(self, request, format=None, pk=None):
        self.object = self.get_object()
        phone_code = self.request.data.get('phone_code', None)

        if self.object.phone_code == phone_code:
            self.object.is_phone_verified = True
            self.object.save()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
