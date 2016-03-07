"""
/home
"""

from pyramid.view import view_config


@view_config(route_name='home', renderer='detectoid:templates/home.pt',
             accept="text/html")
def home(request):
    """
    /home
    """
    return {}
