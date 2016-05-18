from rest_framework import generics

from language.models import Language
from language import serializers


class LanguageMixin(object):
    queryset = Language.objects.all()
    serializer_class = serializers.LanguageSerializer


class LanguageList(LanguageMixin, generics.ListCreateAPIView):
    pass
