from rest_framework import serializers


class ValidateInterestsCount(object):
    def __init__(self):
        self.min = 1
        self.max = 4

    def __call__(self, data):
        if 'interests' not in data:
            return

        interests = data.get('interests', [])
        if not (self.min <= len(interests) <= self.max):
            message = ('You cannot have more than %s interests.' % self.max)
            raise serializers.ValidationError(message)


class ValidateProfilersCount(object):
    def __init__(self):
        self.max = 7

    def __call__(self, instance):
        if instance.photos.count() > self.max:
            message = ('You cannot have more than %s photos.' % (self.max))
            raise serializers.ValidationError(message)
