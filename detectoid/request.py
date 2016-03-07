import pkg_resources

import pyramid.request
from pyramid.decorator import reify

from detectoid.model import get_session


class Request(pyramid.request.Request):

    @reify
    def db(self):
        """
        """
        return get_session()

    @reify
    def version(self):
        """
        """
        return pkg_resources.get_distribution('detectoid').version
