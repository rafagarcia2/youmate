import hashlib

from django import template
from django.conf import settings


register = template.Library()


@register.filter
def get_error_class(field):
    classes = ['validate']
    if field.errors:
        classes.append('invalid')
    return ' '.join(classes)


@register.filter
def exists_pk(queryset, pk):
    return queryset.filter(pk=pk).exists()


@register.filter
def get_profile_photo(user):
    from core.models import Profile
    if isinstance(user, Profile):
        user = user.user

    social = user.socialaccount_set.first()

    if user.profile.photo:
        return '{0}{1}'.format(
            settings.HOST_URL,
            user.profile.photo.url)

    if social:
        return social.get_avatar_url()

    return 'http://www.gravatar.com/avatar/{}?s=40&d=mm'.format(
        hashlib.md5(user.email).hexdigest())


@register.filter
def is_mate_with(from_user, to_user):
    return from_user.profile.mates.filter(
        user_id=to_user.user.id
    ).exists()


@register.filter
def is_interest_selected(profile, interest_id):
    return profile.interests.filter(
        id=interest_id
    ).exists()


@register.filter
def as_range(value):
    return range(value or 0)


@register.filter
def jogo_de_interesse(profile):
    from core.models import Profile
    interests = profile.interests.all()
    mates_ids = list(profile.mates_from.values_list('id', flat=True))
    mates_ids.extend(profile.mates_to.values_list('id', flat=True))
    return Profile.objects.filter(
        interests__in=interests
    ).exclude(
        id=profile.id,
        id__in=mates_ids,
    ).distinct()


@register.filter
def seguranca_em_porcentagem(profile):
    return 100.0 * profile.calcular_seguranca() / 5


@register.filter
def subtract(x, y):
    return x - y


@register.filter
def debuging(item):
    import ipdb; ipdb.set_trace()
