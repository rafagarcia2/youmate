from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.core.exceptions import AppRegistryNotReady


class Profile(models.Model):
    MEN = 'M'
    WOMEN = 'W'
    OTHER = 'X'
    GENRE_CHOICES = (
        (OTHER, _('X')),
        (MEN, _('Men')),
        (WOMEN, _('Women')),
    )

    about = models.TextField(
        _('About'), max_length=400, null=True, blank=True)
    age = models.IntegerField(_('Age'), null=True, blank=True)
    genre = models.CharField(
        _('Genre'), max_length=15, choices=GENRE_CHOICES,
        default=OTHER, null=True, blank=True)
    job_title = models.CharField(
        _('Job title'), max_length=100, null=True, blank=True)
    education = models.CharField(
        _('Education'), max_length=100, null=True, blank=True)
    born_city = models.CharField(
        _('Born city'), max_length=100, null=True, blank=True)
    living_city = models.CharField(
        _('Living city'), max_length=100, null=True, blank=True)

    # relations
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def get_absolute_url(self):
        return reverse_lazy('profile')


class SearchQuery(models.Model):
    living_city = models.CharField(
        _('Living city'), max_length=100, null=True, blank=True)
    start = models.DateField(_('Start'), null=True, blank=True)
    end = models.DateField(_('End'), null=True, blank=True)
    count = models.IntegerField(default=1)

    # relations
    profile = models.ForeignKey('core.Profile')

    class Meta:
        verbose_name = _('Search')
        verbose_name_plural = _('Searchs')
        unique_together = ('living_city', 'start', 'end', 'profile')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except AppRegistryNotReady:
    from django.contrib.auth.models import User

post_save.connect(create_user_profile, sender=User)
