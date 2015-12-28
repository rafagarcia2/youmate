from django.db import models
from django.utils.translation import ugettext as _


class Language(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    locale = models.CharField(
        _('Locale'), max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __unicode__(self):
        return self.name
