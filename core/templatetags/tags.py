import hashlib

from django import template
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
    social = user.socialaccount_set.first()

    if social:
        return social.get_avatar_url()

    return 'http://www.gravatar.com/avatar/{}?s=40&d=mm'.format(
        hashlib.md5(user.email).hexdigest())
