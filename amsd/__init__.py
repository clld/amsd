from pyramid.config import Configurator
from clld.interfaces import IContribution

# we must make sure custom models are known at database initialization!
from amsd import models

_ = lambda s: s
_('Contributor')
_('Contributors')
_('Contribution')
_('Contributions')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    return config.make_wsgi_app()
