from django.db import models
from django.utils.translation import ugettext as _

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
        from django.db.models import *
        return self.answers.annotate(
            likes=Case(
                answer_rates__rate=AnswerRate.LIKE,
                then=Value(1),
                output_field=IntegerField()
            )
        ).order_by('-likes')


class Answer(models.Model):
    created_at = CreationDateTimeField()
    text = models.TextField(
        _('Text'), max_length=400, null=True, blank=True)

    author = models.ForeignKey(to='core.Profile', related_name='answers')
    poll = models.ForeignKey(to='poll.Poll', related_name='answers')

    def __unicode__(self):
        return self.text

    @property
    def likes(self):
        return self.answer_rates.filter(rate=AnswerRate.LIKE).count()

    @property
    def deslikes(self):
        return self.answer_rates.filter(rate=AnswerRate.DESLIKE).count()


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
