from django.db import models
from django.utils.translation import ugettext as _


class Poll(models.Model):
    text = models.CharField(_('Text'), max_length=200)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    author = models.ForeignKey(to='core.Profile', related_name='polls_users')

    class Meta:
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')

    def __unicode__(self):
        return self.text

    @property
    def likes(self):
        return self.polls_rates.filter(rate=PollRate.LIKE).count()

    @property
    def deslikes(self):
        return self.polls_rates.filter(rate=PollRate.DESLIKE).count()


class PollRate(models.Model):
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
        to='core.Profile', related_name='polls_rates')
    poll = models.ForeignKey(
        to='poll.Poll', related_name='polls_rates')

    class Meta:
        verbose_name = _('Poll Rate')
        verbose_name_plural = _('PollR ates')
