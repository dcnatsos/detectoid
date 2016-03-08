"""
/streams end-points
"""

from pyramid.view import view_config

from detectoid.twitch import Twitch


@view_config(route_name='streams', renderer='json')
def streams(request):
    """
    /streams
    """
    return {
        'streams': Twitch().streams(),
    }
