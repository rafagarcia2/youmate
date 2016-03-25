import string
import random

from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from twilio.rest import TwilioRestClient
from push_notifications.models import APNSDevice, GCMDevice
from geopy.geocoders import Nominatim

from core.templatetags.tags import get_profile_photo
from reference.models import Reference
from mate.models import Mate


def code_generate(size=6):
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(size))


def code_generate6():
    return code_generate(6)


def code_generate32():
    return code_generate(32)


class CoreUser(AbstractUser):
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


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

    # Confirmations
    is_email_verified = models.BooleanField(default=False)
    email_code = models.CharField(
        max_length=50, default=code_generate32)
    is_phone_verified = models.BooleanField(default=False)
    phone_code = models.CharField(max_length=50, default=code_generate6)

    # relations
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    mates = models.ManyToManyField(
        to='self', symmetrical=False,
        through='mate.Mate', related_name='mates_related_to+')
    languages = models.ManyToManyField(
        to='language.Language', related_name='profiles')

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return self.user.get_full_name() or str(self.pk)

    def get_absolute_url(self):
        return reverse_lazy('profile')

    def get_device_registration_ids(self):
        registration_ids = []
        registration_ids.extend(
            self.user.gcmdevice_set.values_list('registration_id', flat=True)
        )
        registration_ids.extend(
            self.user.apnsdevice_set.values_list('registration_id', flat=True)
        )
        return set(registration_ids)

    def update_latlong(self):
        if not self.living_city:
            return

        geolocator = Nominatim()
        location = geolocator.geocode(self.living_city)
        self.user.latitude, self.user.longitude = location.point[:-1]
        self.user.save()

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_instance = Profile.objects.get(pk=self.pk)
            if old_instance.phone != self.phone:
                self.send_phone_verification()
            if old_instance.living_city != self.living_city:
                self.update_latlong()

        return super(Profile, self).save(*args, **kwargs)

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

    @property
    def get_photo_url(self):
        return get_profile_photo(self.user)

    @property
    def get_photos(self):
        return [
            '{0}{1}'.format(settings.HOST_URL, photo.image.url)
            for photo in self.photos.all()
        ]

    @property
    def mates_users(self):
        return CoreUser.objects.filter(
            models.Q(
                profile__mates_to__from_user=self,
                profile__mates_to__status=Mate.MATE
            ) |
            models.Q(
                profile__mates_from__from_user=self,
                profile__mates_from__status=Mate.MATE
            ) |
            models.Q(
                profile__mates_to__to_user=self,
                profile__mates_to__status=Mate.MATE
            ) |
            models.Q(
                profile__mates_from__to_user=self,
                profile__mates_from__status=Mate.MATE
            )
        ).exclude(pk=self.user.pk).distinct()

    @property
    def pending_mates(self):
        return self.mates_to.filter(status=Mate.PENDING)

    @property
    def peding_mates_users(self):
        User = auth.get_user_model()
        return User.objects.filter(
            id__in=self.pending_mates.values_list('from_user__user', flat=True)
        )

    @property
    def all_mates(self):
        return Mate.objects.filter(
            models.Q(from_user=self) | models.Q(to_user=self)
        ).distinct()

    def accept_mate(self, profile):
        mate = self.pending_mates.get(from_user=profile)
        mate.accept()

    def reject_mate(self, profile):
        mate = self.pending_mates.get(from_user=profile)
        mate.reject()

    def delete_mate(self, profile):
        mate = Mate.objects.filter(
            models.Q(from_user=self, to_user=profile) |
            models.Q(to_user=self, from_user=profile),
            status=Mate.MATE
        ).first()
        mate.delete()

    def cancel_mate(self, profile):
        mate = Mate.objects.filter(
            from_user=self, to_user=profile, status=Mate.PENDING
        ).first()
        mate.delete()

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
    def get_pretty_referece(self):
        return {
            'total': Reference.objects.filter(to_user=self).count(),
            'average_rate': self.get_average_rate()
        }

    @property
    def get_interests_images(self):
        return map(lambda x: x.get_image_url, self.interests.all())

    def add_mate(self, profile, status='P'):
        mate, created = Mate.objects.get_or_create(
            from_user=self,
            to_user=profile,
            status=status
        )
        # if symm:
        #     # avoid recursion by passing `symm=False`
        #     profile.add_mate(self, status, False)
        return mate

    def get_mate_status(self, profile):
        mate = Mate.objects.filter(
            models.Q(from_user=profile, to_user=self) |
            models.Q(to_user=profile, from_user=self)
        ).first()

        return mate.status if mate else None

    def reset_email_code(self):
        self.email_code = code_generate32()
        self.is_email_verified = False
        self.save()

    def reset_phone_code(self):
        self.phone_code = code_generate6()
        self.is_phone_verified = False
        self.save()

    def send_email_verification(self, reset_email=True):
        if reset_email:
            self.reset_email_code()

        # Send confirmation email
        activate_url = '{host}{confirmation_url}'.format(
            host=settings.HOST_URL,
            confirmation_url=reverse(
                'confirmation_email',
                kwargs={'email_code': self.email_code}
            )
        )
        context = {
            'user_display': self.user.get_full_name() or self.user.email,
            'site_name': 'Youmate',
            'activate_url': activate_url,
        }
        message = render_to_string(
            'account/email/email_confirmation_message.txt', context)
        subject = _(u'Email Confirmation - Youmate')
        recipients = [self.user.email]
        send_mail(subject, message, 'noreply@youmate.com.br', recipients)

    def send_phone_verification(self, reset_phone=True):
        if not settings.ENABLE_SMS:
            return

        if reset_phone:
            self.reset_phone_code()

        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        body = _('To confirm this phone is correct, '
                 'put this code in the app "{{ phone_code }}".')
        client.messages.create(
            body=body.format(phone_code=self.phone_code),
            to=self.phone,
            from_="+NNNNNNNNNNNN",
        )

    def get_device(self, device_id):
        try:
            device = GCMDevice.objects.get(
                device_id=int(device_id),
                user_id=self.user_id,
            )
        except:
            try:
                device = APNSDevice.objects.get(
                    device_id=device_id,
                    user_id=self.user_id,
                )
            except:
                device = None

        return device

    def logout(self, device_id=None):
        device = self.get_device(device_id)

        if not device:
            raise ValueError

        device.active = False
        device.save()


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

        instance.profile.send_email_verification(reset_email=False)


post_save.connect(create_user_profile, sender=CoreUser)
