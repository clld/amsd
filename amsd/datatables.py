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
            AmsdLongTextFieldCol(self, 'description', model_col=MessageStick.description),
            AmsdLongTextFieldCol(self, 'message', model_col=MessageStick.message),
            Col(self, 'date_created', model_col=MessageStick.date_created, sTitle='Date Created'),
            AmsdThumbnailCol(self, 'image', sTitle='Image'),
            # CitationCol(self, 'cite'),
            DetailsRowLinkCol(self, 'more'),
        ]

class AmsdThumbnailCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return item.get_images()


class AmsdLongTextFieldCol(Col):
    def format(self, item):
        v = self.get_value(item)
        if not v:
            return ''
        return v[:100] + '...' if len(v) > 100 else v

def includeme(config):
    config.register_datatable('contributors', AmsdContributors)
    config.register_datatable('contributions', AmsdContributions)
