from zope.interface import classImplements
from pyramid.config import Configurator

from clld.db.models.common import Contribution_files
from clld.interfaces import IMapMarker, IContribution
from clld.web.icon import MapMarker
from clldutils import svg

from amsd import models
from amsd.interfaces import IImage

classImplements(Contribution_files, IImage)

_ = lambda s: s
_('Contributor')
_('Contributors')
_('Contribution')
_('Contributions')


class AmsdMapMarker(MapMarker):
    def __call__(self, ctx, req):
        color, shape = None, 'c'

        if IContribution.providedBy(ctx):
            color = ctx.jsondata['color']

        if color:
            if color.startswith('#'):
                color = color[1:]
            return svg.data_url(svg.icon(shape + color))

        return super(AmsdMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.register_resource('image', Contribution_files, IImage, with_index=True)
    config.registry.registerUtility(AmsdMapMarker(), IMapMarker)
    return config.make_wsgi_app()
