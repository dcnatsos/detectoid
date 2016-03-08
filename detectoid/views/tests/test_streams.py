import unittest

from mock import patch  # NOQA
from pyramid import testing

from detectoid.views.streams import streams


class StreamsTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @patch("detectoid.twitch.Twitch.streams")
    def test_streams(self, twitch_streams):
        """
        """
        request = testing.DummyRequest()

        twitch_streams.return_value = [
            {
                "name": "foo",
                "chatters": 100,
                "viewers": 200,
                "followers": 1200,
                "views": 3000,
            },
        ]

        result = streams(request)

        self.assertEqual(len(result["streams"]), 1)
        self.assertEqual(result["streams"][0]["name"], "foo")
