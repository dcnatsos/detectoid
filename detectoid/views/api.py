"""
"""

from pyramid.view import view_config
import pyramid.httpexceptions as exc

from detectoid.twitch import Twitch


@view_config(route_name='stream', renderer="json")
def stream(request):
    """
    /{stream}

    - stream: stream name

    Returns basic stream info (viewers, chatters, followers, etc)
    """
    name = request.matchdict["stream"].lower()
    info = Twitch().stream(name)

    if info is None:
        raise exc.HTTPInternalServerError("Error while loading stream details {}".format(name))  # NOQA

    if info is False:
        raise exc.HTTPNotFound("Offline stream {}".format(name))

    return {
        'stream': info,
    }

@view_config(route_name='directory', renderer="json")
@view_config(route_name='directory', renderer='detectoid:templates/directory.pt',
             accept="text/html")
@view_config(route_name='directory_game', renderer="json")
@view_config(route_name='directory_game', renderer='detectoid:templates/directory.pt',
             accept="text/html")
def directory(request):
    """
    /directory/all
    /directory/{game}

    - game: sub-section of the directory

    Returns basic stream info (viewers, chatters, followers, etc) for the top 20
    streams in a section
    """
    try:
        game = request.matchdict["game"]
    except KeyError:
        game = None

    info = Twitch().streams(game)

    if info is None:
        raise exc.HTTPInternalServerError("Error while loading streams details {}".format(section))  # NOQA

    if info is False:
        raise exc.HTTPNotFound("Unknown section {}".format(section))

    return {
        'streams': info,
    }


@view_config(route_name='chatters', renderer="json")
def chatters(request):
    """
    /{stream}

    - stream: stream name

    Returns a list of chatters with their registration date
    """
    channel = request.matchdict["stream"].lower()
    users = Twitch().chatters(channel)

    if users is None:
        raise exc.HTTPInternalServerError("Error while loading channel details {}".format(channel))

    return {
        'chatters': users,
    }
