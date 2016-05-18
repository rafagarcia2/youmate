from rest_framework.exceptions import NotAuthenticated
from rest_framework import generics, filters

from reference import serializers
from reference.models import Reference


class ReferenceMixin(object):
    queryset = Reference.objects.all()
    serializer_class = serializers.ReferenceSerializer


class ReferenceList(ReferenceMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'from_user', 'to_user')

    def post(self, request, format=None, pk=None):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()

        request.data.update(
            from_user=str(self.request.user.profile.pk)
        )

        return super(ReferenceList, self).post(
            request=request, format=format, pk=pk)


class ReferenceUpdateView(ReferenceMixin,
                          generics.RetrieveUpdateAPIView):
    pass
