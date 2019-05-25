from clld.web.datatables import (
    Contributors, Contributions)
from clld.web.datatables.base import (
    Col, LinkCol, DetailsRowLinkCol)
from clld.web.datatables.contributor import (
    ContributionsCol)
from clld.db.models.common import (
    Contribution)
from amsd.models import (
    MessageStick)

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
            Col(self, 'message', model_col=MessageStick.message),
            Col(self, 'date_created', sTitle='Date Created'),
            DetailsRowLinkCol(self, 'more'),
        ]

def includeme(config):
    config.register_datatable('contributors', AmsdContributors)
    config.register_datatable('contributions', AmsdContributions)
