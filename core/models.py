from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.core.exceptions import AppRegistryNotReady

from reference.models import Reference
from core.templatetags.tags import get_profile_photo


class Profile(models.Model):
    # Genre choices
    MEN = 'M'
    WOMEN = 'W'
    OTHER = 'X'
    GENRE_CHOICES = (
        (OTHER, _('X')),
        (MEN, _('Men')),
        (WOMEN, _('Women')),
    )

    # Status choices
    LOCAL = 'L'
    TRAVELER = 'T'
    STATUS_CHOICES = (
        (LOCAL, _('Local')),
        (TRAVELER, _('Traveler')),
    )

    about = models.TextField(
        _('About'), max_length=400, null=True, blank=True)
    age = models.IntegerField(_('Age'), null=True, blank=True)
    genre = models.CharField(
        _('Genre'), max_length=15, choices=GENRE_CHOICES,
        default=OTHER, null=True, blank=True)
    status = models.CharField(
        _('Status'), max_length=15, choices=STATUS_CHOICES,
        null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=40, null=True, blank=True)
    job_title = models.CharField(
        _('Job title'), max_length=100, null=True, blank=True)
    education = models.CharField(
        _('Education'), max_length=100, null=True, blank=True)
    born_city = models.CharField(
        _('Born city'), max_length=100, null=True, blank=True)
    living_city = models.CharField(
        _('Living city'), max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    # relations
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    mates = models.ManyToManyField(
        to='self', symmetrical=False,
        through='mate.Mate', related_name='mates_by')
    languages = models.ManyToManyField(
        to='language.Language', related_name='profiles')

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def get_absolute_url(self):
        return reverse_lazy('profile')

    @property
    def reference(self):
        reference = Reference.objects.filter(
            to_user=self, active=True
        ).first()
        return reference

    @property
    def ultimas_referencias(self):
        return Reference.objects.filter(
            to_user=self
        ).order_by('-created_at')[:3]

    @property
    def has_phone(self):
        return True if self.phone else False

    def calcular_seguranca(self):
        criterias = [
            self.user.is_active,
            self.user.is_active,
            self.has_phone,
            self.references_to.exists(),
            self.references_to.exists(),
        ]
        return len(filter(lambda x: x is True, criterias))

    def get_average_rate(self):
        return int(Reference.objects.filter(
            to_user=self
        ).aggregate(
            models.Avg('rating')
        )['rating__avg'] or 0)

    @property
    def get_photo_url(self):
        return get_profile_photo(self.user)


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
