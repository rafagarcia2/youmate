from rest_framework import generics

from mate.models import Mate
from mate import serializers


class MateMixin(object):
    queryset = Mate.objects.all()
    serializer_class = serializers.MateSerializer


class MateList(MateMixin, generics.ListCreateAPIView):
    pass


class MateUpdateView(MateMixin, generics.RetrieveUpdateAPIView):
    pass
