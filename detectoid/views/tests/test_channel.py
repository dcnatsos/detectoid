import unittest
import datetime

from mock import Mock, patch  # NOQA
from pyramid import testing
import pyramid.httpexceptions as exc

from detectoid.views.channel import chatters, distribution  # NOQA
from detectoid.model.user import User


class ChannelTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @patch("detectoid.twitch.Twitch.chatters")
    def test_chatters(self, twitch_chatters):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'channel': "foobarbaz"}

        now = datetime.datetime.now()
        twitch_chatters.return_value = [
            User(name="foo", created=now, updated=now, follows=1),
            User(name="bar", created=now, updated=now, follows=1),
        ]

        result = chatters(request)

        self.assertEqual(len(result["chatters"]), 2)
        self.assertEqual(result["chatters"][0].__json__(Mock())["name"], "foo")

    @patch("detectoid.twitch.Twitch.chatters", return_value=None)
    def test_chatters_500(self, twitch_chatters):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'channel': "foobarbaz"}
        self.assertRaises(exc.HTTPInternalServerError,
                          lambda: chatters(request))

    @patch("detectoid.twitch.Twitch.chatters")
    def test_distribution(self, twitch_chatters):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'channel': "foobarbaz"}

        now = datetime.datetime.now()
        twitch_chatters.return_value = [
            User(name="foo", created=now, updated=now, follows=1),
            User(name="bar", created=now, updated=now, follows=1),
        ]

        result = distribution(request)

        self.assertEqual(len(result["distribution"]), 1)
        self.assertEqual(result["distribution"][0]["count"], 2)

    @patch("detectoid.twitch.Twitch.chatters", return_value=None)
    def test_distribution_500(self, chatters):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'channel': "foobarbaz"}
        self.assertRaises(exc.HTTPInternalServerError,
                          lambda: distribution(request))
