from clld.web.datatables import (
    Contributors, Contributions)
from clld.web.datatables.base import (
    Col, LinkCol, DetailsRowLinkCol)
from clld.web.datatables.contributor import (
    ContributionsCol)
from clld.web.datatables.contribution import (
    CitationCol, ContributorsCol)
from clld.db.models.common import (
    Contribution)
from amsd.models import (
    MessageStick)
from clld.web.util.htmllib import HTML
from pprint import pprint

class AmsdContributors(Contributors):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            ContributionsCol(self, 'Contributions', sTitle='Data set'),
        ]

class AmsdContributions(Contributions):
    def col_defs(self):
        return [
            LinkCol(self, 'id', model_col=Contribution.id),
            Col(self, 'title', model_col=MessageStick.title),
            AmsdLongTextFieldCol(self, 'message', model_col=MessageStick.message),
            Col(self, 'date_created', model_col=MessageStick.date_created, sTitle='Date Created'),
            AmsdThumbnailCol(self, 'linked_filenames', sTitle='Image'),
            # CitationCol(self, 'cite'),
            DetailsRowLinkCol(self, 'more'),
        ]

class AmsdThumbnailCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return item.get_linked_filenames(item.linked_filenames, 'thumbnail')


class AmsdLongTextFieldCol(Col):
    def format(self, item):
        return item.message[:100] + '...' if len(item.message) > 100 else item.message

def includeme(config):
    config.register_datatable('contributors', AmsdContributors)
    config.register_datatable('contributions', AmsdContributions)
