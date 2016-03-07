
import os
import json
import datetime
from unittest import TestCase

from mock import Mock, patch  # NOQA

from detectoid.model import get_session
from detectoid.model.user import User
from detectoid.twitch import Twitch, parse_date  # NOQA

class TwitchTests(TestCase):

    def setUp(self):
        self.db = get_session()

    def create_user(self, username):
        created = datetime.datetime.now()
        updated = created + datetime.timedelta(days=10)
        user = User(name=username, created=created, updated=updated, follows=8)

        self.db.add(user)
        self.db.flush()

        return user

    def test_load_json_decode_error(self):
        """
        """
        twitch = Twitch()
        twitch.tcp.get = Mock(side_effect=json.decoder.JSONDecodeError('a', 'b', 10))  # NOQA

        self.assertEqual(None, twitch._load_json("bar"))

    def test_load_json_type_error(self):
        """
        """
        twitch = Twitch()
        twitch.tcp.get = Mock(side_effect=TypeError)

        self.assertEqual(None, twitch._load_json("baz"))

    def test_streams(self):
        """
        """
        stream = {
            "streams": [{
                "viewers": 25,
                "channel": {
                    "name": "foo",
                    "views": 1000,
                    "followers": 200,
                },
            }]
        }
        chatters = {
            "chatters": {
                "viewers": ["foo", "bar", "baz"]
            }
        }

        twitch = Twitch()
        mock_response = Mock()
        mock_response.json.side_effect = [stream, chatters]
        twitch.tcp.get = Mock(return_value=mock_response)

        result = twitch.streams()

        self.assertEqual(1, len(result))
        self.assertEqual(result[0]["chatters"],
                         len(chatters["chatters"]["viewers"]))
        self.assertEqual(result[0]["viewers"],
                         stream["streams"][0]["viewers"])
        self.assertEqual(result[0]["followers"],
                         stream["streams"][0]["channel"]["followers"])
        self.assertEqual(result[0]["views"],
                         stream["streams"][0]["channel"]["views"])

    @patch('detectoid.twitch.Twitch._load_json', return_value=None)
    def test_streams_failed(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch.streams())

    @patch('detectoid.twitch.Twitch._list_chatters', return_value=None)
    def test_streams_bogus(self, _list_chatters):
        """
        """
        stream = {
            "streams": [{
                "viewers": 25,
                "channel": {
                    "name": "foo",
                    "views": 1000,
                    "followers": 200,
                },
            }]
        }

        twitch = Twitch()
        mock_response = Mock()
        mock_response.json.return_value = stream
        twitch.tcp.get = Mock(return_value=mock_response)

        self.assertNotEqual(None, twitch.streams())

    def test_chatters(self):
        """
        """
        username = "viewer"
        user = self.create_user(username)
        chatters = {
            "chatters": {
                "viewers": [username]
            }
        }
        twitch = Twitch()
        mock_response = Mock()
        mock_response.json.return_value = chatters
        twitch.tcp.get = Mock(return_value=mock_response)

        self.assertEqual(twitch.chatters("foo"), [user])

    @patch('detectoid.twitch.Twitch._load_json', return_value=None)
    def test_chatters_failed(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch.chatters("bar"))

    @patch('detectoid.twitch.Twitch._load_json', return_value={})
    def test_chatters_bogus(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch.chatters("boo"))

    def test_user(self):
        """
        """
        twitch = Twitch()
        user = self.create_user("foobar")

        self.assertEqual(user, twitch.user(user.name))

    def test_user_load(self):
        """
        """
        record = {
            "name": "bazbar",
            "created_at": "2016-02-26T17:29:16Z",
            "updated_at": "2016-03-26T17:29:16Z",
        }

        twitch = Twitch()
        twitch._user_profile = Mock(return_value=record)
        twitch._user_follows = Mock(return_value=None)

        user = twitch.user(record["name"])

        self.assertEqual(user.name, record["name"])
        self.assertEqual(user.created, parse_date(record["created_at"]))
        self.assertEqual(user.updated, parse_date(record["updated_at"]))
        self.assertEqual(user.follows, 0)

    def test_user_load_failed(self):
        """
        """
        twitch = Twitch()
        twitch._user_profile = Mock(return_value=None)

        self.assertEqual(None, twitch.user("foo11"))

    def test_user_profile(self):
        """
        """
        record = {
            "name": "bazbar",
            "created_at": "2016-02-26T17:29:16Z",
            "updated_at": "2016-03-26T17:29:16Z",
        }
        twitch = Twitch()
        mock_response = Mock()
        mock_response.json.return_value = record
        twitch.tcp.get = Mock(return_value=mock_response)

        self.assertEqual(record, twitch._user_profile("randomuser"))

    @patch('detectoid.twitch.Twitch._load_json', return_value=None)
    def test_user_profile_failed(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch._user_profile("bar23"))

    @patch('detectoid.twitch.Twitch._load_json', return_value={})
    def test_user_profile_bogus(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch._user_profile("bar23"))

    @patch('detectoid.twitch.Twitch._load_json', return_value={"_total": 420})
    def test_user_follows(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(420, twitch._user_follows("randomuser34"))

    @patch('detectoid.twitch.Twitch._load_json', return_value=None)
    def test_user_follows_failed(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch._user_follows("bar45"))

    @patch('detectoid.twitch.Twitch._load_json', return_value={})
    def test_user_follows_bogus(self, _load_json):
        """
        """
        twitch = Twitch()

        self.assertEqual(None, twitch._user_follows("bar43"))
