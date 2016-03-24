from datetime import datetime, date

from django.core.files.base import ContentFile

from requests import request, HTTPError
from geopy.geocoders import Nominatim


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

    if gender == 'male':
        user.profile.gender = 'M'
    elif gender == 'female':
        user.profile.gender = 'W'

    if backend.name == 'facebook':
        location = response.get('location', {}).get('name')
        if location:
            user.profile.living_city = location

        if birthday:
            user.profile.age = convert_birthday(birthday)

    if backend.name == 'google-oauth2':
        places_lived = response.get('placesLived')
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
        geolocator = Nominatim()
        location = geolocator.geocode(user.profile.living_city)
        user.latitude, user.longitude = location.point[:-1]
        user.save()
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
