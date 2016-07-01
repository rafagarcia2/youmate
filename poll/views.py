from django.db import connection

from rest_framework import generics, views, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from geopy.geocoders import Nominatim

from poll import serializers
from poll.models import Poll, Answer


class PollMixin(object):
    queryset = Poll.objects.all()
    serializer_class = serializers.PollSerializer


class AnswerMixin(object):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class PollList(PollMixin, generics.ListCreateAPIView):
    filter_fields = {
        'text': ['icontains'],
        # 'custom_filters': [
        #     'latitude', 'longitude', 'address', 'interests__id', 'text'
        # ]
    }

    def get_queryset(self):
        queryset = super(PollList, self).get_queryset()
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

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
                location = geolocator.geocode(
                    profile.living_city.split('-')[0])
                try:
                    latitude, longitude = location.point[:-1]
                except:
                    pass

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
                    FROM poll_poll
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

        interests_ids = self.request.query_params.get(
            'interests__id') or None
        try:
            interests_ids = interests_ids.split(',')
        except AttributeError:
            pass

        if isinstance(interests_ids, list):
            queryset = queryset.filter(
                interests__id__in=interests_ids
            )

        queryset = queryset.distinct()
        return queryset


class PollCreateView(PollMixin, generics.CreateAPIView):
    serializer_class = serializers.PollCreateSerializer

    def post(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

        latitude = longitude = None
        address = self.request.data.pop('address', None)

        if address:
            geolocator = Nominatim()
            location = geolocator.geocode(address)
            try:
                latitude, longitude = location.point[:-1]
            except:
                location = geolocator.geocode(
                    profile.living_city.split('-')[0])
                try:
                    latitude, longitude = location.point[:-1]
                except:
                    pass

        if latitude is not None and longitude is not None:
            request.data.update(
                latitude='{0:.6f}'.format(latitude),
                longitude='{0:.6f}'.format(longitude),
            )

        request.data.update(
            author=profile.pk
        )

        return super(PollCreateView, self).post(
            request=request, format=format, pk=pk)


class PollDetailView(PollMixin, generics.RetrieveDestroyAPIView):
    def delete(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

        self.object = self.get_object()
        if profile == self.object.author:
            raise ValidationError('You can only delete your own polls.')

        return super(PollDetailView, self).delete(
            request, format=format, pk=pk)


class PollUpdateView(PollMixin, generics.UpdateAPIView):
    serializer_class = serializers.PollUpdateSerializer


class AnswerList(AnswerMixin, generics.ListAPIView):
    def get_queryset(self):
        return self.queryset.filter(**self.kwargs)


class AnswerCreateView(AnswerMixin, generics.CreateAPIView):
    serializer_class = serializers.AnswerCreateSerializer

    def get_queryset(self):
        return self.queryset.filter(**self.kwargs)

    def get_poll(self):
        from poll.models import Poll
        return Poll.objects.get(pk=self.kwargs.get('poll__pk'))

    def post(self, request, format=None, pk=None, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

        request.data.update(
            poll=self.get_poll().id,
            author=profile.pk
        )

        return super(AnswerCreateView, self).post(
            request=request, format=format, pk=pk, *args, **kwargs)


class AnswerUpdateView(AnswerMixin, generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def delete(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

        self.object = self.get_object()
        if profile not in [self.object.author, self.object.poll.author]:
            raise ValidationError('You can only delete your own answers.')

        return super(PollDetailView, self).delete(
            request, format=format, pk=pk)


class AnswerLikeView(AnswerMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def post(self, request, *args, **kwargs):
        from poll.models import AnswerRate

        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

        self.object = self.get_object()

        already_liked = profile.answer_rates.filter(
            answer=self.object, rate=AnswerRate.LIKE
        ).exists()

        if already_liked:
            message = ('You can only like a answer once.')
            return Response(
                {'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile.like_answer(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AnswerDeslikeView(AnswerMixin, views.APIView):
    def get_object(self):
        return self.queryset.get(**self.kwargs)

    def post(self, request, *args, **kwargs):
        from poll.models import AnswerRate

        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        profile = self.request.user.profile

        self.object = self.get_object()

        already_liked = profile.answer_rates.filter(
            answer=self.object, rate=AnswerRate.LIKE
        ).exists()

        if not already_liked:
            message = ('You cant deslike a answer that you never liked.')
            return Response(
                {'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile.deslike_answer(self.object)
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
