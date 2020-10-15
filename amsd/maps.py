# from pyramid.renderers import render
from clld.web.maps import Layer, Map
from clld.web.adapters.geojson import GeoJson
from clld.db.meta import DBSession
import amsd.models

_CONTRIBUTION_MAP_OPTIONS = {
    'info_route': 'contribution_alt',
    'hash': True,
    'zoom': 4,
    'max_zoom': 15,
    'base_layer': 'OpenTopoMap',
    'show_labels': False,
}


class GeoJsonSelectedContributions(GeoJson):
    def __init__(self, pk=None):
        if pk:
            self.obj = DBSession.query(amsd.models.MessageStick)\
                .filter(amsd.models.MessageStick.pk == pk)
        else:
            self.obj = DBSession.query(amsd.models.MessageStick)\
                .filter(amsd.models.MessageStick.latitude is not None)

    def feature_iterator(self, ctx, req):
        return self.obj.all()

    def featurecollection_properties(self, ctx, req):
        return {'layer': 'Message Sticks'}

    def feature_properties(self, ctx, req, valueset):
        return {
            'item': valueset,
            'label': valueset.id
        }


class SelectedContributionsMap(Map):
    def get_options(self):
        return {
            **_CONTRIBUTION_MAP_OPTIONS,
            'info_query': {'map_pop_up': 1},
            'center': (-26.51, 138.34),
        }

    def get_layers(self):
        yield Layer(
            self.req.translate('Contributions'),
            self.req.translate('Contributions'),
            GeoJsonSelectedContributions()
                .render(self.ctx, self.req, dump=False),
        )


class SelectedContributionMap(Map):
    def get_options(self):
        return {
            **_CONTRIBUTION_MAP_OPTIONS,
            'no_popup': True,
            'no_link': True,
            'sidebar': True,
        }

    def get_layers(self):
        yield Layer(
            self.req.translate('Contribution'),
            self.req.translate('Contribution'),
            GeoJsonSelectedContributions(self.ctx.pk)
                .render(self.ctx, self.req, dump=False))


def includeme(config):
    config.register_map('contributions', SelectedContributionsMap)
    config.register_map('contribution', SelectedContributionMap)
