"""
Django settings for youmate project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf import global_settings

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8gm$c$+&w6#n*$bmc_4i%f=)c)oft9(u*c-d@_)jh9@gx3r&_9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOST_URL = 'http://youmate.herokuapp.com'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

MEDIA_ROOT = 'media'

MEDIA_URL = '/media/'

MANDRILL_API_KEY = "YW3aJkoPhCmodizEU7ZGvQ"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

# Application definition

DJANGO_APPS = (
    # The Django sites framework is required
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

LOCAL_APPS = (
    'core',
    'mate',
    'reference',
    'language',
    'photo',
    'interest',
    'api',
)

EXTERNAL_APPS = (
    'django_extensions',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_filters',
    'rest_auth',
    'rest_auth.registration',
    'corsheaders',
    'oauth2_provider',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    'push_notifications',
    'django_twilio',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + EXTERNAL_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


ROOT_URLCONF = 'youmate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ),
        },
    },
]

WSGI_APPLICATION = 'youmate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DEFAULT_DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

DATABASES = {
    'default': dj_database_url.config() or DEFAULT_DATABASE
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Django allauth

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    # Django
    'django.contrib.auth.backends.ModelBackend',

    # Social auth
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
)

# Social auth configuration
SOCIAL_AUTH_FACEBOOK_KEY = '1685351455020151'
SOCIAL_AUTH_FACEBOOK_SECRET = '5dc0a60e3812301c576211452ac6cce8'
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
    'public_profile',
    'user_about_me',
    'user_birthday',
    'user_location',
    'user_location',
]
SOCIAL_AUTH_FACEBOOK_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
    'public_profile',
    'user_location'
]

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ('79881842751-c9l225d7nojbqhsfeuak1h8mlmqmmlgi'
                                 '.apps.googleusercontent.com')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '26mT_rgQys1saUiCeqzgjjCB'

# AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
#     'oauth2_provider.backends.OAuth2Backend',
#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',

#     'rest_framework_social_oauth2.backends.DjangoOAuth2',
#     'django.contrib.auth.backends.ModelBackend',

#     # Facebook OAuth2
#     'social.backends.facebook.FacebookAppOAuth2',
#     'social.backends.facebook.FacebookOAuth2',
# )

# MIDDLEWARE_CLASSES = global_settings.AUTHENTICATION_BACKENDS + (
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware'
# )

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    )
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    },
    # Expire after a month
    'ACCESS_TOKEN_EXPIRE_SECONDS': 2592000,
}


PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_API_KEY': 'AIzaSyDVqU9aA_gi71GnCN6nxka0EK-3ijZketg',
    # 'APNS_CERTIFICATE': '/path/to/your/certificate.pem',
}

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_ADAPTER = 'core.adapter.AccountAdapter'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True

# Twilio config
ENABLE_SMS = False
TWILIO_ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
TWILIO_AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
TWILIO_DEFAULT_CALLERID = 'NNNNNNNNNN'


# Import the custom settings
try:
    from local_settings import *
except ImportError:
    pass
