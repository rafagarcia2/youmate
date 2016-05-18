from rest_framework import generics

from interest import serializers
from interest.models import Interest


class InterestMixin(object):
    queryset = Interest.objects.all()
    serializer_class = serializers.InterestSerializer


class InterestList(InterestMixin, generics.ListCreateAPIView):
    pass


class InterestUpdateView(InterestMixin,
                         generics.RetrieveUpdateAPIView):
    pass

