from datetime import datetime, date


def convert_birthday(birthday):
    birthday = datetime.strptime(birthday, '%m/%d/%Y').date()
    today = date.today()
    return (
        today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day)
        )
    )


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        birthday = response.get('birthday')
        if birthday:
            user.profile.age = convert_birthday(birthday)
        user.profile.save()
