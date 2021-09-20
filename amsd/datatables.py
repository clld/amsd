import re

from clld.web.datatables import Contributors, Contributions, Sources
from clld.web.datatables.base import DataTable, Col, LinkCol, DetailsRowLinkCol, LinkToMapCol
from clld.web.datatables.contributor import ContributionsCol
from clld.db.models.common import Contribution
from clldutils.misc import nfilter
from amsd.models import MessageStick, keywords, x_keywords
from clld.db.util import icontains

from sqlalchemy import or_, func
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

        # define which datatable column should be appear for prefiltering
        self.remote_fields = [5, 6]

        # init prefilters
        for c in ['sem_domain', 'keywords'] + ['sSearch_{0}'.format(i) for i in self.remote_fields]:
            setattr(self, c, None)
            if c in req.params:
                setattr(self, c, req.params[c].split(','))
                if len(getattr(self, c)) and not len(getattr(self, c)[0]):
                    setattr(self, c, None)

    def base_query(self, query):
        contr_pks = set()
        # prefiltering
        was_prefiltered = False
        prefilter_tables = ['sem_domain', 'keywords']
        for c in prefilter_tables:
            v = getattr(self, c)
            if v:
                was_prefiltered = True
                cm = getattr(amsd.models, c)
                xcm = getattr(amsd.models, 'x_%s' % (c))
                qf = [cm.name == q for q in v]
                q = set(DBSession.query(xcm.object_pk)
                        .filter(xcm.item_pk.in_(DBSession.query(cm.pk).filter(or_(*qf))))
                        .group_by(xcm.object_pk)
                        .having(func.count(xcm.object_pk) == len(qf)))
                contr_pks = contr_pks & q if contr_pks else q

        if was_prefiltered:
            query = query.filter(Contribution.pk.in_([i for i, in contr_pks]))

        return query.outerjoin(x_keywords, keywords).options(
            joinedload(MessageStick._files)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'id', model_col=Contribution.id),
            AmsdLongTextFieldCol(self, 'title', model_col=MessageStick.title),
            AmsdThumbnailCol(self, 'image', sTitle='Image'),
            DetailsRowLinkCol(self, 'more'),
            LinkToMapCol(self, 'm'),
            AmsdFtsCol(self, 'any_text_field', model_col=MessageStick.fts),
            Col(self, 'message', model_col=MessageStick.message, bVisible=False),
        ]


def get_ts_search_string(s_):
    """Converts a search string into a ts_query conform syntax
    - a " " will be replaced by " & "
    - a :* will be append to each search term for partial matching ("starts with")
    """
    # if any special character appear return None to let handle plainto_tsquery() the search
    if any(e in s_ for e in ["'", '*', ':', '&', '|', '(', ')', '!']):
        return None

    # while creating tsvector
    # _ and - will be replaced by . to avoid tokenizing
    # ,\t\r\n – will be replaced by 'space' to take them as search separator
    s = re.sub(r'[,\t\r\n]', ' ', re.sub(r'[_\-]', '.', s_))

    search_items = set(nfilter(re.split(' +', s.replace('"', ''))))
    search_items = nfilter([a.strip() for a in search_items])
    return ' & '.join(['%s:*' % (a) for a in search_items])


class AmsdFtsCol(Col):
    __kw__ = dict(
        sDescription="Search for terms, separated by spaces, in all text fields. "
        "The search is word initial, it ignores English stop words like "
        "'a', 'from', 'the', etc., and it includes English inflection.",
        bSortable=False,
        bVisible=False,
        bSearchable=False)

    def format(self, item):
        return ''

    def search(self, qs):
        qs_ = get_ts_search_string(qs)
        if qs_:
            query = func.to_tsquery('english', qs_)
        else:
            query = func.plainto_tsquery('english', qs)
        return self.model_col.op('@@')(query)


class AmsdThumbnailCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        return item.get_images(req=self.dt.req)


class AmsdLongTextFieldCol(Col):
    def format(self, item):
        v = self.get_value(item)
        if not v:  # pragma: no cover
            return ''
        return v[:130] + '...' if len(v) > 130 else v


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
