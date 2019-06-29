from __future__ import unicode_literals, absolute_import, division, print_function

from zope.interface import classImplements
from pyramid.config import Configurator

from clld.db.models.common import Contribution_files

from amsd import models
from amsd.interfaces import IImage

classImplements(Contribution_files, IImage)

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
    config.register_resource('image', Contribution_files, IImage, with_index=True)
    return config.make_wsgi_app()
