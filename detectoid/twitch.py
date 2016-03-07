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

    def chatters(self, channel):
        """
        Returns a list of users logged into a chat channel
        """
        try:
            r = self.tcp.get(endpoints['chatters'].format(channel))
            r = r.json()

            return [self.user(name) for name in r["chatters"]["viewers"]]
        except json.decoder.JSONDecodeError:
            logger.exception("error while loading %s", channel)
        except TypeError:
            logger.exception("error while loading %s", channel)

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
        try:
            r = self.tcp.get(endpoints['profile'].format(username))
            r = r.json()

            if "created_at" in r:
                return r
        except json.decoder.JSONDecodeError:
            logger.warning("bogus user record received for %s", username)

    def _user_follows(self, username):
        """
        Returns the number of channels followed by a user
        """
        try:
            r = self.tcp.get(endpoints['follows'].format(username))
            r = r.json()

            if "_total" in r:
                return r["_total"]
        except json.decoder.JSONDecodeError:
            logger.warning("bogus follows record received for %s", username)
