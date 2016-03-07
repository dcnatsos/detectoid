"""
Global config file
"""

import os

from paste.deploy.loadwsgi import appconfig

config = None


def set_config(settings):
    """
    Set the config from a dictionnary
    """
    global config

    config = settings


def get_config():
    """
    Returns a global configuration object as a dictionnary

    Raise IOError if the config is not loaded and we can't fallback on tests.ini.
    """
    global config

    if config is None:
        here = os.path.dirname(__file__)
        config = appconfig('config:' + os.path.join(here, '../', 'tests.ini'))
    return config
