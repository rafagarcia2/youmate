from django.contrib import auth
from push_notifications.models import APNSDevice, GCMDevice

from api import serializers

from interest.models import Interest
from reference.models import Reference
from language.models import Language
from photo.models import Photo
from core.models import Profile
from mate.models import Mate


class UserMixin(object):
    queryset = auth.get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class UserFeedMixin(UserMixin):
    serializer_class = serializers.UserFeedSerializer


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
