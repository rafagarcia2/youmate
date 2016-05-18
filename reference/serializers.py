from rest_framework import serializers

from reference.models import Reference


class ReferenceSerializer(serializers.ModelSerializer):
    from_user__photo_url = serializers.CharField(
        source='from_user.get_photo_url', read_only=True)
    from_user__pk = serializers.CharField(
        source='from_user.user.pk', read_only=True)
    from_user__first_name = serializers.CharField(
        source='from_user.user.first_name', read_only=True)
    from_user__last_name = serializers.CharField(
        source='from_user.user.last_name', read_only=True)
    to_user__pk = serializers.CharField(
        source='to_user.user.pk', read_only=True)

    class Meta:
        model = Reference

    def validate_users_are_mate(self, data):
        from_user = data.get('from_user')
        to_user = data.get('to_user')
        if not from_user.mates_users.filter(profile=to_user).exists():
            message = ('You can only create references for your mates.')
            raise serializers.ValidationError(message)

    def validate(self, data):
        self.validate_users_are_mate(data=data)
        return super(ReferenceSerializer, self).validate(data)
