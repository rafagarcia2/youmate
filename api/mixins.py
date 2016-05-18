from push_notifications.models import APNSDevice, GCMDevice

from api import serializers


class APNSDeviceMixin(object):
    queryset = APNSDevice.objects.all()
    serializer_class = serializers.APNSDeviceSerializer


class GCMDeviceMixin(object):
    queryset = GCMDevice.objects.all()
    serializer_class = serializers.GCMDeviceSerializer
