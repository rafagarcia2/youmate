from django.conf import settings
from django.shortcuts import resolve_url
from django.core.urlresolvers import reverse

from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        url = settings.LOGIN_REDIRECT_URL
        threshold = 90
        logged_time = request.user.last_login - request.user.date_joined

        if logged_time.seconds < threshold:
            url = reverse('profile'),

        return resolve_url(url)
