from datetime import datetime

from django.db import models
from django.db.models.signals import post_save

from django_extensions.db.fields import CreationDateTimeField


class Mate(models.Model):
    PENDING = 'P'
    MATE = 'M'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (MATE, 'Mate'),
    )

    from_user = models.ForeignKey(
        to='core.Profile', related_name='mates_from')
    to_user = models.ForeignKey(
        to='core.Profile', related_name='mates_to')
    created_at = CreationDateTimeField()
    status = models.CharField(
        choices=STATUS_CHOICES,
        default=PENDING,
        max_length=2)

    class Meta:
        verbose_name = 'Mate'
        verbose_name_plural = 'Mates'

    def get_mates(self, status):
        return self.mates.filter(
            to_user__from_user=self)

    def get_mates_with_me(self, status):
        return self.mates_with_me.filter(
            from_user__to_user=self)

    def get_mates_together(self):
        return self.mates.filter(
            to_user__from_user=self,
            from_user__to_user=self
        )

    def get_following(self):
        return self.get_mates()

    def get_followers(self):
        return self.get_mates_with_me()

    def accept(self):
        self.status = self.MATE
        self.save()

    def reject(self):
        self.delete()


def send_mate_notification(sender, instance, **kwargs):
    if instance.status != Mate.PENDING:
        return

    from_name = (
        instance.from_user.user.first_name or
        instance.from_user.user.username
    )
    message = '{} quer ser seu Mate.'.format(from_name)
    photo_url = instance.from_user.get_photo_url
    devices = list(instance.to_user.user.gcmdevice_set.filter(active=True))
    devices.extend(instance.to_user.user.apnsdevice_set.filter(active=True))
    notification_id = int(
        (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    )

    data = {
        'title': 'YouMate',
        'message': message,
        'image': photo_url,
        'type': 'invite_mate',
        'mateId': str(instance.from_user.id),
        'notId': str(notification_id),
    }
    for device in devices:
        try:
            device.send_message(message, extra=data)
        except:
            pass


def accepted_mate_notification(sender, instance, **kwargs):
    if instance.status != Mate.MATE:
        return

    to_name = (
        instance.to_user.user.first_name or
        instance.to_user.user.username
    )
    message = '{} aceitou ser seu Mate.'.format(to_name)
    photo_url = instance.to_user.get_photo_url
    devices = list(instance.from_user.user.gcmdevice_set.filter(active=True))
    devices.extend(
        instance.from_user.user.apnsdevice_set.filter(active=True))
    notification_id = int(
        (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    )

    data = {
        'title': 'YouMate',
        'message': message,
        'image': photo_url,
        'type': 'accept_mate',
        'mateId': str(instance.to_user.id),
        'notId': str(notification_id),
    }
    for device in devices:
        device.send_message(message, extra=data)

post_save.connect(send_mate_notification, sender=Mate)
post_save.connect(accepted_mate_notification, sender=Mate)
