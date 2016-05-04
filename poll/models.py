from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.db.models import Sum, F

from django_extensions.db.fields import CreationDateTimeField


class Poll(models.Model):
    text = models.CharField(_('Text'), max_length=200)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    author = models.ForeignKey(to='core.Profile', related_name='polls')

    class Meta:
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')

    def __unicode__(self):
        return self.text

    def get_sorted_answers(self):
        return self.answers.annotate(
            rate=Sum(F('likes') - F('deslikes'))
        ).order_by('-rate', 'created_at')

    @property
    def get_interests_images(self):
        return map(lambda x: x.get_image_url, self.interests.all())


class Answer(models.Model):
    created_at = CreationDateTimeField()
    text = models.TextField(
        _('Text'), max_length=400, null=True, blank=True)
    likes = models.IntegerField(_('Likes'), default=0)
    deslikes = models.IntegerField(_('Deslikes'), default=0)

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
    DESLIKE = 'D'
    RATE_CHOICES = (
        (LIKE, _('Like')),
        (DESLIKE, _('Deslike')),
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
        else:
            instance.answer.deslikes += 1
        instance.answer.save()


post_save.connect(update_like_answer, sender=AnswerRate)
