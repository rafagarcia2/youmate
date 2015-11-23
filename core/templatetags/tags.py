import hashlib

from django import template

from core.models import Profile

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
    if isinstance(user, Profile):
        user = user.user

    social = user.socialaccount_set.first()

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
    return range(value)


@register.filter
def jogo_de_interesse(profile):
    interests = profile.interests.all()
    return Profile.objects.filter(
        interests__in=interests
    ).distinct()


@register.filter
def seguranca_em_porcentagem(profile):
    return 100.0 * profile.calcular_seguranca() / 5
