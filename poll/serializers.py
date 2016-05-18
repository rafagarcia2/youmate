from rest_framework import serializers

from poll.models import Poll, Answer

from api.validators import ValidateInterestsCount
from core.serializers import PollProfileSerializer
from interest.serializers import FeedInterestSerializer


class AnswerSerializer(serializers.ModelSerializer):
    user = PollProfileSerializer(
        source='author', read_only=True
    )
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ('id', 'user', 'text', 'likes', 'liked')

    def get_liked(self, instance):
        if not self.context['request'].user.is_authenticated():
            return None

        profile = self.context['request'].user.profile
        return instance.has_being_liked_by(profile=profile)


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'author', 'text', 'poll')


class PollSerializer(serializers.ModelSerializer):
    user = PollProfileSerializer(
        source='author'
    )
    interests = FeedInterestSerializer(many=True, read_only=True)
    answers = AnswerSerializer(
        many=True, read_only=True,
        source='get_sorted_answers'
    )

    class Meta:
        model = Poll
        fields = ('id', 'text', 'user', 'interests', 'answers')
        validators = [
            ValidateInterestsCount()
        ]


class PollCreateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False)

    class Meta:
        model = Poll
        fields = (
            'id', 'text', 'author', 'interests',
            'latitude', 'longitude', 'address'
        )
        validators = [
            ValidateInterestsCount()
        ]


class PollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'text', 'interests')
        validators = [
            ValidateInterestsCount()
        ]


class ProfilePollsSerializer(serializers.ModelSerializer):
    polls = PollSerializer(
        source='polls',
        many=True,
        read_only=True
    )

    class Meta:
        from core.models import Profile
        model = Profile
        fields = ('polls',)
