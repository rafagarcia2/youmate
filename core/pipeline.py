from datetime import datetime, date


def convert_birthday(birthday, date_format='%m/%d/%Y'):
    birthday = datetime.strptime(birthday, date_format).date()
    today = date.today()
    return (
        today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day)
        )
    )


def save_profile(backend, user, response, *args, **kwargs):
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
    user.profile.save()
