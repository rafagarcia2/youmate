from django.db import models

from django_extensions.db.fields import CreationDateTimeField


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    created_at = CreationDateTimeField()

    # relations
    profile = models.ForeignKey(to='core.Profile', related_name='photos')

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
