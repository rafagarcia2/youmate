from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.staticfiles.templatetags.staticfiles import static


class Interest(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    description = models.TextField(
        _('Description'), max_length=400, null=True, blank=True)
    image_class = models.CharField(_('Image'), max_length=50, null=True)

    profiles = models.ManyToManyField(
        to='core.Profile', related_name='interests')
    polls = models.ManyToManyField(
        to='poll.Poll', related_name='interests')

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    def __unicode__(self):
        return self.title

    @property
    def get_image_url(self):
        photo = static('images/interests/{}.svg'.format(self.image_class))
        return '{host}{photo}'.format(host=settings.HOST_URL, photo=photo)
