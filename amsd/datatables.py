from clld.web.datatables import (
    Contributors, Contributions, Sources)
from clld.web.datatables.base import (
    DataTable, Col, LinkCol, DetailsRowLinkCol,
    LinkToMapCol)
from clld.web.datatables.contributor import (
    ContributionsCol)
from clld.web.datatables.contribution import (
    CitationCol, ContributorsCol)
from clld.db.models.common import (
    Contribution, Source, ContributionReference, Contribution_files)
from clldutils.misc import nfilter
from amsd.models import (
    MessageStick,
    sem_domain, x_sem_domain,
    material, x_material,
    technique, x_technique,
    keywords, x_keywords,
    ling_area, item_type,
    holder_file, source_type, x_source_type)
from clld.web.util.htmllib import HTML
from clld.db.util import icontains

from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload, aliased
from clld.db.meta import DBSession

import amsd.models
import re

_LING_AREA_1 = aliased(ling_area)
_LING_AREA_2 = aliased(ling_area)
_LING_AREA_3 = aliased(ling_area)
_X_FIELDS = {
            keywords.name: x_keywords,
            material.name: x_material,
            technique.name: x_technique,
            sem_domain.name: x_sem_domain,
            source_type.name: x_source_type,
        }
_REL_FIELDS = [
            item_type.name,
            holder_file.name,
            Contribution_files.name,
        ]
_SPEC_FIELDS = {
            _LING_AREA_1.chirila_name: MessageStick.ling_area_1,
            _LING_AREA_2.chirila_name: MessageStick.ling_area_2,
            _LING_AREA_3.chirila_name: MessageStick.ling_area_3,
            _LING_AREA_1.austlang_code: MessageStick.ling_area_1,
            _LING_AREA_2.austlang_code: MessageStick.ling_area_2,
            _LING_AREA_3.austlang_code: MessageStick.ling_area_3,
            _LING_AREA_1.austlang_name: MessageStick.ling_area_1,
            _LING_AREA_2.austlang_name: MessageStick.ling_area_2,
            _LING_AREA_3.austlang_name: MessageStick.ling_area_3,
            _LING_AREA_1.glottolog_code: MessageStick.ling_area_1,
            _LING_AREA_2.glottolog_code: MessageStick.ling_area_2,
            _LING_AREA_3.glottolog_code: MessageStick.ling_area_3,
            Source.name: ContributionReference,
        }
_STICK_FIELDS = [getattr(MessageStick, col.name)\
        for col in MessageStick.__table__.columns if str(col.type) == 'VARCHAR']
_STICK_FIELDS.extend([Contribution.description, Contribution.id])

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
        self.sf_global = None
        if 'sf_global' in req.params:
            self.sf_global = req.params['sf_global']
            if not len(self.sf_global):
                self.sf_global = None

    def base_query(self, query):

        contr_pks = set()

        # prefiltering
        prefilter_tables = ['sem_domain', 'material', 'technique', 'keywords']
        for c in prefilter_tables:
            v = getattr(self, c)
            if v:
                cm = getattr(amsd.models, c)
                xcm = getattr(amsd.models, 'x_%s' % (c))
                qf = [cm.name == q for q in v]
                q = set(DBSession.query(xcm.object_pk) \
                    .filter(xcm.item_pk.in_(DBSession.query(cm.pk).filter(or_(*qf)))) \
                    .group_by(xcm.object_pk) \
                    .having(func.count(xcm.object_pk) == len(qf)))
                contr_pks = contr_pks & q if contr_pks else q

        # global search prefiltering
        if self.sf_global:
            # split search items by spaces not occuring in double quotes (à la Google)
            # ==> a d "b c" d c -> ['a', 'b c', 'd', 'c']
            quote_cnt = self.sf_global.count('"')
            if quote_cnt == 0: # no quotes
                search_items = set(nfilter(re.split(' +', self.sf_global)))
            elif quote_cnt % 2: # odd number of quotes
                search_items = set(nfilter(re.split(' +', self.sf_global.replace('"', ''))))
            else:
                search_items = set([a.strip().replace('"', '')\
                        for a in nfilter(re.split(' +(?=([^\"]*\"[^\"]*\")*[^\"]*$)', self.sf_global))\
                            if (a.startswith('"') and a.endswith('"'))\
                                    or (not a.startswith('"') and not a.endswith('"'))])

            if len(search_items) > 8:
                search_items = list(search_items)[:8]

            for i, qs in enumerate(search_items):
                pks = set()
                for col in _X_FIELDS:
                    pks.update(DBSession.query(Contribution.pk)\
                        .join(_X_FIELDS[col])\
                        .join(col.class_)\
                        .filter(icontains(col, qs)).distinct().all())
                for col in _REL_FIELDS:
                    pks.update(DBSession.query(Contribution.pk)\
                        .outerjoin(col.class_)\
                        .filter(icontains(col, qs)).distinct().all())
                for col in _SPEC_FIELDS:
                    pks.update(DBSession.query(Contribution.pk)\
                        .outerjoin(_SPEC_FIELDS[col])\
                        .filter(icontains(col, qs)).distinct().all())
                for col in _STICK_FIELDS:
                    pks.update(DBSession.query(Contribution.pk)\
                        .filter(icontains(col, qs)).distinct().all())
                if not i:
                    contr_pks = contr_pks & pks if contr_pks else pks
                else:
                    contr_pks = contr_pks & pks
            if not contr_pks:
                contr_pks = [(0,)]

        if contr_pks:
            query = query.filter(Contribution.pk.in_(contr_pks))
        return query.outerjoin(x_keywords, keywords).options(
            joinedload(MessageStick._files)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'id', model_col=Contribution.id),
            Col(self, 'title', model_col=MessageStick.title),
            AmsdLongTextFieldCol(self, 'description', model_col=MessageStick.description),
            AmsdLongTextFieldCol(self, 'message', model_col=MessageStick.message),
            AmsdThumbnailCol(self, 'image', sTitle='Image'),
            XCol(self, 'keywords'),
            DetailsRowLinkCol(self, 'more'),
            LinkToMapCol(self, 'm'),
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
