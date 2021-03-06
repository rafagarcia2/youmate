from datetime import datetime, date

from django.core.files.base import ContentFile

from requests import request, HTTPError


def convert_birthday(birthday, date_format='%m/%d/%Y'):
    birthday = datetime.strptime(birthday, date_format).date()
    today = date.today()
    return (
        today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day)
        )
    )


def save_profile(backend, user, response, *args, **kwargs):
    if not kwargs.get('is_new'):
        return

    birthday = response.get('birthday')
    gender = response.get('gender')

    if backend.name == 'facebook':
        user.email = response.get('email')

        if gender == 'masculino':
            user.profile.gender = 'M'
        elif gender == 'feminino':
            user.profile.gender = 'W'

        location = response.get('location', {}).get('name')
        if location:
            user.profile.living_city = location

        if birthday:
            user.profile.age = convert_birthday(birthday)

    if backend.name == 'google-oauth2':
        if gender == 'male':
            user.profile.gender = 'M'
        elif gender == 'female':
            user.profile.gender = 'W'

        if not user.email:
            try:
                user.email = response.get('emails')[0].get('value')
                user.save()
            except:
                pass

        places_lived = response.get('placesLived')

        if places_lived is not None:
            try:
                user.profile.living_city = places_lived[-1].get('value')
            except IndexError:
                pass

        if birthday and not birthday.startswith('0000-'):
            try:
                user.profile.age = convert_birthday(birthday, '%Y-%m-%d')
            except ValueError:
                pass

    if not (user.latitude and user.longitude) and user.profile.living_city:
        user.profile.update_latlong()
    user.profile.save()


def save_profile_picture(backend, user, response, *args, **kwargs):
    if not kwargs.get('is_new'):
        return

    url = None
    params = {}

    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        params = {'type': 'large'}

    if backend.name == 'google-oauth2' and response.get('image'):
        url = response['image'].get('url').replace('?sz=50', '')

    try:
        response = request('GET', url, params=params)
        response.raise_for_status()
    except HTTPError:
        pass
    else:
        user.profile.photo.save(
            '{0}_photo.jpg'.format(user.username),
            ContentFile(response.content))
        user.profile.save()
