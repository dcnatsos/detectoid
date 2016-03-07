#!/usr/bin/env python
"""
destructoid
------------------------------
Destructoid, a simple website to guess whether a Twitch stream has viewbots
"""

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')

    config.scan(ignore='destructoid.tests')

    return config.make_wsgi_app()
