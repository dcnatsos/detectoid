import unittest
import datetime

from mock import Mock, patch  # NOQA
from pyramid import testing
import pyramid.httpexceptions as exc

from detectoid.views.api import stream, distribution  # NOQA
from detectoid.model.user import User


class ChannelTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @patch('detectoid.twitch.Twitch._load_json')
    @patch('detectoid.twitch.Twitch._list_chatters')
    def test_channel(self, list_chatters, load_json):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'stream': "foobar"}

        load_json.return_value = {
            "stream": {
                "viewers": 2025,
                "channel": {
                    "display_name":"foobar",
                    "views": 4164868,
                    "followers": 110218,
                }
            }
        }

        list_chatters.return_value = ["foo", "bar", "baz"]

        result = stream(request)

        self.assertEqual(result["stream"]["name"],
                         load_json.return_value["stream"]["channel"]["display_name"])  # NOQA
        self.assertEqual(result["stream"]["viewers"],
                         load_json.return_value["stream"]["viewers"])
        self.assertEqual(result["stream"]["views"],
                         load_json.return_value["stream"]["channel"]["views"])
        self.assertEqual(result["stream"]["followers"],
                         load_json.return_value["stream"]["channel"]["followers"])  # NOQA
        self.assertEqual(result["stream"]["chatters"], 3)

    @patch('detectoid.twitch.Twitch._load_json', return_value=None)
    def test_channel_invalid_channel(self, load_json):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'stream': "foobarbaz"}
        self.assertRaises(exc.HTTPInternalServerError, lambda: stream(request))

    @patch('detectoid.twitch.Twitch._load_json')
    def test_channel_offline_channel(self, load_json):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'stream': "foobarbaz"}

        load_json.return_value = {"stream": None}

        self.assertRaises(exc.HTTPNotFound, lambda: stream(request))

    @patch("detectoid.twitch.Twitch.chatters")
    def test_distribution(self, twitch_chatters):
        """
        """
        request = testing.DummyRequest()
        request.matchdict = {'stream': "foobarbaz"}

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
        request.matchdict = {'stream': "foobarbaz"}
        self.assertRaises(exc.HTTPInternalServerError,
                          lambda: distribution(request))
