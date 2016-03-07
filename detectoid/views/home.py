"""
/ homepage
"""

from pyramid.view import view_config

from detectoid.twitch import Twitch


@view_config(route_name='home', renderer='detectoid:templates/home.pt',
             accept="text/html")
def home(request):
    """
    /
    """
    return {
        'streams': Twitch().streams(),
    }
