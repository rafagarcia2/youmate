from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save, pre_delete

from django_extensions.db.fields import CreationDateTimeField


class Poll(models.Model):
    created_at = CreationDateTimeField()
    text = models.CharField(_('Text'), max_length=400)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    author = models.ForeignKey(to='core.Profile', related_name='polls')

    class Meta:
        ordering = ['created_at']
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')

    def __unicode__(self):
        return self.text

    def get_sorted_answers(self):
        return self.answers.order_by('-likes', 'created_at')

    @property
    def get_interests_images(self):
        return map(lambda x: x.get_image_url, self.interests.all())


class Answer(models.Model):
    created_at = CreationDateTimeField()
    text = models.TextField(
        _('Text'), max_length=400, null=True, blank=True)
    likes = models.IntegerField(_('Likes'), default=0)

    author = models.ForeignKey(to='core.Profile', related_name='answers')
    poll = models.ForeignKey(to='poll.Poll', related_name='answers')

    def __unicode__(self):
        return self.text

    def has_being_liked_by(self, profile):
        return AnswerRate.objects.filter(
            answer=self,
            created_by=profile,
            rate=AnswerRate.LIKE
        ).exists()


class AnswerRate(models.Model):
    # Genre choices
    LIKE = 'L'
    RATE_CHOICES = (
        (LIKE, _('Like')),
    )
    rate = models.CharField(
        _('Rate'), max_length=2, choices=RATE_CHOICES, default=LIKE)

    created_by = models.ForeignKey(
        to='core.Profile', related_name='answer_rates')
    answer = models.ForeignKey(
        to='poll.Answer', related_name='answer_rates')

    class Meta:
        verbose_name = _('Answer Rate')
        verbose_name_plural = _('Answer Rates')


def update_like_answer(sender, instance, created, **kwargs):
    if created:
        if instance.rate == AnswerRate.LIKE:
            instance.answer.likes += 1
            instance.answer.save()


def deslike_answer(sender, instance, **kwargs):
    instance.answer.likes -= 1
    instance.answer.save()


def send_answer_notification(sender, instance, created, **kwargs):
    if not created:
        return

    from_name = (
        instance.author.user.first_name or
        instance.author.user.username
    )
    message = '{} respondeu sua pergunta.'.format(from_name)
    photo_url = instance.author.get_photo_url
    devices = list(instance.poll.author.user.gcmdevice_set.filter(active=True))
    devices.extend(
        instance.poll.author.user.apnsdevice_set.filter(active=True))
    notification_id = int(
        (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    )

    data = {
        'title': 'YouMate',
        'message': message,
        'image': photo_url,
        'type': 'answer_poll',
        'pollId': str(instance.id),
        'profileId': str(instance.author.id),
        'notId': str(notification_id),
    }
    for device in devices:
        device.send_message(message, extra=data)


def send_like_answer_notification(sender, instance, created, **kwargs):
    if not created and not instance.rate == AnswerRate.LIKE:
        return

    from_name = (
        instance.created_by.user.first_name or
        instance.created_by.user.username
    )
    message = '{} curtiu sua resposta.'.format(from_name)
    photo_url = instance.created_by.get_photo_url
    devices = list(
        instance.answer.author.user.gcmdevice_set.filter(active=True)
    )
    devices.extend(
        instance.answer.author.user.apnsdevice_set.filter(active=True))
    notification_id = int(
        (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    )

    data = {
        'title': 'YouMate',
        'message': message,
        'image': photo_url,
        'type': 'answer_poll',
        'pollId': str(instance.poll.id),
        'profileId': str(instance.created_by.id),
        'notId': str(notification_id),
    }
    for device in devices:
        device.send_message(message, extra=data)


post_save.connect(send_answer_notification, sender=Answer)
post_save.connect(send_like_answer_notification, sender=AnswerRate)
post_save.connect(update_like_answer, sender=AnswerRate)
pre_delete.connect(deslike_answer, sender=AnswerRate)
