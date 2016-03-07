"""
/{channel} end-points
"""

from pyramid.view import view_config
import pyramid.httpexceptions as exc

from detectoid.twitch import Twitch
from detectoid.utils import group_by_date


@view_config(route_name='chatters', renderer='json')
def chatters(request):
    """
    /{channel}

    - channel: stream name
    """
    channel = request.matchdict["channel"].lower()
    twitch = Twitch()
    users = twitch.chatters(channel)

    if users is None:
        raise exc.HTTPInternalServerError("Error while loading channel details {}".format(channel))

    return {
        'chatters': users,
    }

@view_config(route_name='distribution', renderer='json')
def distribution(request):
    """
    /{channel}/distribution

    - channel: stream name
    """
    channel = request.matchdict["channel"].lower()
    twitch = Twitch()
    users = twitch.chatters(channel)

    if users is None:
        raise exc.HTTPInternalServerError("Error while loading channel details {}".format(channel))

    groups = group_by_date(users)

    return {
        'distribution': [{
                'date': date,
                'count': count,
            }
            for date, count in groups.items()
        ],
    }
