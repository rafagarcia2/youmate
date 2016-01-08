from django.db import models

from django_extensions.db.fields import CreationDateTimeField


class Reference(models.Model):
    RATING_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
    )

    from_user = models.ForeignKey(
        to='core.Profile', related_name='references_from')
    to_user = models.ForeignKey(
        to='core.Profile', related_name='references_to')
    created_at = CreationDateTimeField()
    text = models.TextField(
        'Texto da referencia', max_length=400, null=False, blank=False)
    active = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, default=1)

    class Meta:
        verbose_name = 'Reference'
        verbose_name_plural = 'References'


def set_personal_reference_to_active(sender, instance, created, **kwargs):
    if created and instance.from_user == instance.to_user:
        instance.from_user.references_from.update(active=False)
        instance.active = True
        instance.save()
