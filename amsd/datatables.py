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
from sqlalchemy.orm import joinedload
from clld.db.meta import DBSession

import amsd.models
import re


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
            AmsdFtsCol(self, 'fts', model_col=MessageStick.fts),
            DetailsRowLinkCol(self, 'more'),
            LinkToMapCol(self, 'm'),
        ]

def get_ts_search_string(s_):
    """Converts a search string into a ts_query conform syntax
    - a " " outside of double quotes will be replaced by " & "
    - a " " inside of double quotes will be replaced by " <-> " for phrase search
            and a ":*" (partial match from begin) will be added to the last token
    - a :* will be append to each search term which is not inside double quotes
            for partial matching ("starts with")
    """

    # if any special character appear return None to let handle plainto_tsquery() the search
    if any(e in s_ for e in ["'",'*',':','&','|','(',')','!']):
        return None

    # while creating tsvector _ and - were replaced by . to avoid tokenizing
    s = re.sub('[_\-]','.',s_).replace(',', ' ')

    quote_cnt = s.count('"')
    if quote_cnt == 0: # no quotes
        search_items = set(nfilter(re.split(' +', s)))
    elif quote_cnt % 2: # odd number of quotes -> no quotes
        search_items = set(nfilter(re.split(' +', s.replace('"', ''))))
    else:
        search_items = set([a.strip().replace('"', '')\
                for a in nfilter(re.split(' +(?=([^\"]*\"[^\"]*\")*[^\"]*$)', s))\
                    if (a.startswith('"') and a.endswith('"'))\
                            or (not a.startswith('"') and not a.endswith('"'))])

    search_items = nfilter([a.strip() for a in search_items])

    ret = []
    for a in search_items:
        if ' ' in a: # => double quote token
            a_ = re.split(' +', a)
            a_l = len(a_)
            if a_l > 1:
                ret.append(' <-> '.join(a_[:-1]) + ' <-> %s:*' % (a_[-1]))
            elif a_l == 1:
                ret.append('%s:*' % (a_[0]))
        else:
            ret.append('%s:*' % (a))

    return ' & '.join(ret)

class AmsdFtsCol(Col):
    __kw__ = dict(
        bSortable=False,
        sTitle='Any field',
        sDescription='Search in any field of the Message Stick record',
        sTooltip='Search for terms, separated by spaces, in all text fields. A terms can be wrapped by double quotes for a phrase search. The search starts at the beginnings of words.')

    def format(self, item):
        return ''

    def search(self, qs):
        qs_ = get_ts_search_string(qs)
        if qs_:
            query = func.to_tsquery('english', qs_)
        else:
            query = func.plainto_tsquery('english', qs)
        return self.model_col.op('@@')(query)


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
