from clld.web.datatables import (
    Contributors, Contributions, Sources)
from clld.web.datatables.base import (
    DataTable, Col, LinkCol, DetailsRowLinkCol)
from clld.web.datatables.contributor import (
    ContributionsCol)
from clld.web.datatables.contribution import (
    CitationCol, ContributorsCol)
from clld.db.models.common import (
    Contribution)
from amsd.models import (
    MessageStick,
    sem_domain, x_sem_domain,
    material, x_material,
    technique, x_technique,
    keywords, x_keywords)
from clld.web.util.htmllib import HTML
from clld.db.util import icontains

from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload
from clld.db.meta import DBSession

import amsd.models

class AmsdContributors(Contributors):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            ContributionsCol(self, 'Contributions', sTitle='Data set'),
        ]

class AmsdContributions(Contributions):
    def __init__(self, req, *args, **kw):
        Contributions.__init__(self, req, *args, **kw)
        # init prefilters
        for c in ['sem_domain', 'material', 'technique', 'keywords']:
            setattr(self, c, None)
            if c in req.params:
                setattr(self, c, req.params[c].split(','))
                if len(getattr(self, c)) and not len(getattr(self, c)[0]):
                    setattr(self, c, None)

    def base_query(self, query):
        # prefiltering
        contr_pks = set()
        for c in ['sem_domain', 'material', 'technique', 'keywords']:
            v = getattr(self, c)
            cm = getattr(amsd.models, c)
            xcm = getattr(amsd.models, 'x_%s' % (c))
            if v:
                qf = [cm.name == q for q in v]
                q = [pk for pk, in DBSession.query(xcm.object_pk) \
                    .filter(xcm.item_pk.in_(DBSession.query(cm.pk).filter(or_(*qf)))) \
                    .group_by(xcm.object_pk) \
                    .having(func.count(xcm.object_pk) == len(qf))]
                contr_pks = contr_pks & set(q) if contr_pks else set(q)
            if(contr_pks):
                query = query.filter(Contribution.pk.in_(contr_pks))
            query = query.outerjoin(xcm).outerjoin(cm)
        return query.options(joinedload(MessageStick._files)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'id', model_col=Contribution.id),
            Col(self, 'title', model_col=MessageStick.title),
            AmsdLongTextFieldCol(self, 'description', model_col=MessageStick.description),
            AmsdLongTextFieldCol(self, 'message', model_col=MessageStick.message),
            AmsdThumbnailCol(self, 'image', sTitle='Image'),
            XCol(self, 'material'),
            XCol(self, 'technique'),
            XCol(self, 'keywords'),
            DetailsRowLinkCol(self, 'more'),
        ]

class XCol(Col):
    def get_value(self, item):
        return item.get_x(self.name)
    def order(self):
        return getattr(amsd.models, self.name).name
    def search(self, qs):
        return icontains(getattr(amsd.models, self.name).name, qs)

class AmsdThumbnailCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return item.get_images(req=self.dt.req)


class AmsdLongTextFieldCol(Col):
    def format(self, item):
        v = self.get_value(item)
        if not v:
            return ''
        return v[:100] + '...' if len(v) > 100 else v

class AmsdSources(Sources):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle='Note'),
        ]

class AmsdImages(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'mime_type', sTitle='type'),
        ]

def includeme(config):
    config.register_datatable('contributors', AmsdContributors)
    config.register_datatable('contributions', AmsdContributions)
    config.register_datatable('sources', AmsdSources)
    config.register_datatable('images', AmsdImages)
