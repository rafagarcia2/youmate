from django.conf import settings
from django.utils.translation import ugettext as _

from rest_framework import permissions


class AppSecretKeyPermission(permissions.BasePermission):
    message = _('You are not allowed to see this page.')

    def has_permission(self, request, view):
        app_secret_key = self.request.META.get('APP_SECRET_KEY')
        if self.request.user.is_authenticated():
            is_superuser = self.request.user.is_superuser
        return is_superuser or app_secret_key == settings.APP_SECRET_KEY
