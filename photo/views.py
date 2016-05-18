from rest_framework import generics, filters
from rest_framework.exceptions import NotAuthenticated

from photo.models import Photo
from photo import serializers


class PhotoMixin(object):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer


class PhotoList(PhotoMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = {
        'profile': ['exact'],
    }


class PhotoRetrieveDelete(PhotoMixin, generics.RetrieveDestroyAPIView):
    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        self.object = self.get_object()

        if not self.request.user.is_authenticated() and \
           self.request.user.profile != self.object.profile:
            raise NotAuthenticated()

        return super(PhotoRetrieveDelete, self).delete(
            request, *args, **kwargs)
