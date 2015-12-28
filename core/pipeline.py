from datetime import date
from time import mktime

from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2

from core.models import Profile


def custom_user_details(strategy, details, response, user=None, *args, **kwargs):
    if not user:
        return

    if kwargs['is_new']:
        if isinstance(kwargs.get('backend'), FacebookOAuth2):
            pass
        elif isinstance(kwargs.get('backend'), GoogleOAuth2):
            pass
