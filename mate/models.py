from django.db import models

from django_extensions.db.fields import CreationDateTimeField


class Mate(models.Model):
    PENDING = 'P'
    MATE = 'M'
    BLOCKED = 'B'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (MATE, 'Mate'),
        (BLOCKED, 'Blocked'),
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
        # unique_together = ('from_user', 'to_user')

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
