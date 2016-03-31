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
