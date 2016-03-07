"""
Twitch API consumption
"""

import datetime
import logging

import json
import requests

from detectoid.model import get_session
from detectoid.model.user import User

logger = logging.getLogger()

endpoints = {
    'streams': "https://api.twitch.tv/kraken/streams?limit=10",
    'chatters': "http://tmi.twitch.tv/group/user/{}/chatters",
    'profile': "https://api.twitch.tv/kraken/users/{}",
    'follows': "https://api.twitch.tv/kraken/users/{}/follows/channels?limit=1",
}


def parse_date(string):
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")


class Twitch(object):

    def __init__(self):
        self.tcp = requests.Session()
        self.tcp.headers.update({'client_id': "detectoid_client"})

        self.db = get_session()

    def _load_json(self, uri):
        try:
            return self.tcp.get(uri).json()
        except (json.decoder.JSONDecodeError, TypeError):
            logger.warning("failed to load the json at %s", uri)

    def streams(self):
        """
        Returns a list of top streams with their chatters numbers
        """
        data = self._load_json(endpoints['streams'])

        if data is None:
            logger.warning("no data in streams()")
            return None

        result = []
        for stream in data["streams"]:
            chatters = self._list_chatters(stream["channel"]["name"])

            if chatters is None:
                count = 0
            else:
                count = len(chatters)

            result.append({
                "name": stream["channel"]["name"],
                "chatters": count,
                "viewers": stream["viewers"],
                "followers": stream["channel"]["followers"],
                "views": stream["channel"]["views"],
            })

        return result

    def _list_chatters(self, channel):
        """
        Returns a list of usernames logged into a chat channel
        """
        data = self._load_json(endpoints['chatters'].format(channel))

        if data is None:
            logger.warning("no data in _list_chatters(%s)", channel)
            return None

        if "chatters" not in data:
            logger.warning("bogus data in _list_chatters(%s)", channel)
            return None

        return data["chatters"]["viewers"]

    def chatters(self, channel):
        """
        Returns a list of Users logged into a chat channel
        """
        names = self._list_chatters(channel)

        if names is None:
            return None

        return [self.user(name) for name in names]

    def user(self, username):
        """
        Returns a loaded User object from its username
        """
        # try to load the user record from db
        user = self.db.query(User).filter(User.name == username).one_or_none()

        # if it's a new user, load details and persist it
        if user is None:
            logger.debug("loading new user %s", username)

            # load user profile
            record = self._user_profile(username)

            if record is None:
                return None

            # load follows count
            follows = self._user_follows(username)

            if follows is None:
                follows = 0

            user = User(name=record["name"],
                        created=parse_date(record["created_at"]),
                        updated=parse_date(record["updated_at"]),
                        follows=follows)
            self.db.add(user)

        logger.debug("loaded user %s", username)

        return user

    def _user_profile(self, username):
        """
        Returns a user profile, as a dictionnary, loaded from Twitch
        """
        data = self._load_json(endpoints['profile'].format(username))

        if data is None:
            logger.warning("no data in _user_profile(%s)", username)
            return None

        if "created_at" not in data:
            return None

        return data

    def _user_follows(self, username):
        """
        Returns the number of channels followed by a user
        """
        data = self._load_json(endpoints['follows'].format(username))

        if data is None:
            logger.warning("no data in _user_follows(%s)", username)
            return None

        if "_total" not in data:
            logger.warning("bogus data in _user_follows(%s)", username)
            return None

        return data["_total"]
