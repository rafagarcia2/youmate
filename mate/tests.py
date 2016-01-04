from django.test import TestCase
from django.contrib import auth

from mate.models import Mate


class TestMate(TestCase):
    def setUp(self):
        user1 = auth.get_user_model().objects.create(username='user1')
        user2 = auth.get_user_model().objects.create(username='user2')

        self.profile1 = user1.profile
        self.profile2 = user2.profile

    def test_add_mate(self):
        self.profile1.add_mate(self.profile2)

        self.assertEquals(1, Mate.objects.count())
        self.assertEquals(1, self.profile2.peding_mates.count())
        self.assertEquals(0, self.profile1.mates_profiles.count())
        self.assertEquals(0, self.profile2.mates_profiles.count())

    def test_send_multiple_mates(self):
        self.profile1.add_mate(self.profile2)

        self.assertEquals(1, Mate.objects.count())
        self.assertEquals(1, self.profile2.peding_mates.count())
        self.assertEquals(0, self.profile1.mates_profiles.count())
        self.assertEquals(0, self.profile2.mates_profiles.count())

    def test_accept_mate(self):
        self.profile1.add_mate(self.profile2)

        self.profile2.accept_mate(self.profile1)

        self.assertEquals(1, Mate.objects.count())
        self.assertEquals(0, self.profile2.peding_mates.count())
        self.assertEquals(1, self.profile1.mates_profiles.count())
        self.assertEquals(1, self.profile2.mates_profiles.count())

    def test_reject_mate(self):
        self.profile1.add_mate(self.profile2)

        self.profile2.reject_mate(self.profile1)

        self.assertEquals(0, Mate.objects.count())
        self.assertEquals(0, self.profile2.peding_mates.count())
        self.assertEquals(0, self.profile1.mates_profiles.count())
        self.assertEquals(0, self.profile2.mates_profiles.count())
