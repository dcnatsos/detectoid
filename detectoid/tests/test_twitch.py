
import os
import json
import datetime
from unittest import TestCase

from mock import Mock  # NOQA

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

    def test_chatters_decode_error(self):
        """
        """
        twitch = Twitch()
        twitch.tcp.get = Mock(side_effect=json.decoder.JSONDecodeError('a', 'b', 10))  # NOQA

        self.assertEqual(None, twitch.chatters("bar"))

    def test_chatters_type_error(self):
        """
        """
        twitch = Twitch()
        twitch.tcp.get = Mock(side_effect=TypeError)

        self.assertEqual(None, twitch.chatters("baz"))

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

    def test_user_profile_decode_error(self):
        """
        """
        twitch = Twitch()
        twitch.tcp.get = Mock(side_effect=json.decoder.JSONDecodeError('a', 'b', 10))  # NOQA

        self.assertEqual(None, twitch._user_profile("bar23"))

    def test_user_follows(self):
        """
        """
        twitch = Twitch()
        mock_response = Mock()
        mock_response.json.return_value = {"_total": 420}
        twitch.tcp.get = Mock(return_value=mock_response)

        self.assertEqual(420, twitch._user_follows("randomuser34"))

    def test_user_follows_decode_error(self):
        """
        """
        twitch = Twitch()
        twitch.tcp.get = Mock(side_effect=json.decoder.JSONDecodeError('a', 'b', 10))  # NOQA

        self.assertEqual(None, twitch._user_follows("bar45"))
