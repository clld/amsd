from math import floor

from clld.db.meta import DBSession
from clld.db.models.common import (
    Contributor,
    Contribution,
    Contribution_files,
)
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import get_referents, link
from clld.web.util.multiselect import MultiSelect

from clldmpg import cdstar

import amsd.models


def contribution_index_html(context=None, request=None, **kw):
    q = DBSession.query(amsd.models.MessageStick)
    c_all = q.count()
    c_loc = q.filter(amsd.models.MessageStick.latitude != None).count()
    c_note = None
    if c_loc < c_all:
        c_note = 'Note: only %i of %i message sticks have geographical coordinates' % (
                    c_loc, c_all)
    return dict(
        select_sem_domain = XMultiSelect(context, request, 'sem_domain', 'ms-sem_domain'),
        select_material = XMultiSelect(context, request, 'material', 'ms-material'),
        select_technique = XMultiSelect(context, request, 'technique', 'ms-technique'),
        select_keywords = XMultiSelect(context, request, 'keywords', 'ms-keywords'),
        count_loc_note = c_note,
    )

def contribution_detail_html(context=None, request=None, **kw):
    return {
        'data_entry': get_data_entry(context, request),
        'semantic_domains': get_x_data('sem_domain', context, request),
        'materials': get_x_data('material', context, request),
        'techniques': get_x_data('technique', context, request),
        'source_types': get_x_data('source_type', context, request),
        'linked_filename_urls': context.get_images(image_type='web', width='', req=request),
    }

def dataset_detail_html(context=None, request=None, **kw):
    example_image_name = '20161106-ebay-s-l1600_0.jpg'
    example = None
    try:
        example_context = DBSession.query(Contribution_files) \
                    .filter(Contribution_files.name == example_image_name).all()[0]
        example = {
            'link_url': '%s/%s' % (request.route_url('images'), example_context.id),
            'image_url': cdstar.bitstream_url(example_context)}
    except:
        pass
    return {
        'count_sticks': len(DBSession.query(amsd.models.MessageStick).all()),
        'count_ling_areas': len(DBSession.query(amsd.models.ling_area).all()),
        'example': example,
        'count_terms': len(DBSession.query(
                amsd.models.MessageStick.stick_term)
                    .filter(amsd.models.MessageStick.stick_term != '')
                    .distinct().all()),
    }

def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(
        context, exclude=['valueset', 'sentence', 'language'])}

def get_sticks(source):
    res = {}
    obj_pks = DBSession.query(Contribution_files.object_pk).filter(
            Contribution_files.name == source.name).distinct().all()
    q = DBSession.query(Contribution).filter(Contribution.pk.in_(obj_pks)).distinct()
    res[Contribution.__name__.lower()] = q.all()
    return res

def image_detail_html(context=None, request=None, **kw):
    referents = get_sticks(context)
    if context.mime_type == 'application/pdf':
        return {'referents': referents,
                'image': HTML.div(
                            HTML.iframe(
                                class_='pdf_iframe',
                                src='%sbitstreams/%s/%s' % (
                                    cdstar.SERVICE_URL, context.jsondata.get('refobjid'), context.jsondata.get('original')),
                                frameborder='0',
                            ),
                            class_='div_pdf_iframe',
                        )}
    else:
        return {'referents': referents,
                'image': HTML.img(
                            class_='image_single',
                            src = cdstar.bitstream_url(context),
                        ),
                    }

def amsd_linked_references(req, obj):
    chunks = []
    for ref in sorted(getattr(obj, 'references', []), key=lambda x: x.source.note or ''):
        if ref.source:
            chunks.append(HTML.li(
                HTML.span(link(req, ref.source), class_='citation')
            ))
    if chunks:
        return HTML.span(*chunks)
    return ''

def get_popup_images(req, obj):
    imgs = obj.get_images(req=req, image_type='web')
    if imgs:
        return "%s<br /><br />" % (imgs)
    return ""

def get_x_data(model_name=None, context=None, request=None, **kw):
    m = getattr(amsd.models, model_name)
    x_m =  getattr(amsd.models, 'x_%s' % (model_name))
    q = [n for n, in DBSession.query(m.name) \
                .join(x_m) \
                .filter(x_m.object_pk == context.pk) \
                .order_by(m.name)]
    return ', '.join(q)

def get_data_entry(context=None, request=None, **kw):
    res = []
    if not context.data_entry:
        return None
    for r in context.data_entry.split(';'):
        for f in DBSession.query(Contributor).filter(Contributor.id == r):
            res.append(HTML.a(f.name, href='%s/%s' % (request.route_url('contributors'), r)))
    return ', '.join(res)

def degminsec(dec, hemispheres):
    _dec = abs(dec)
    degrees = int(floor(_dec))
    _dec = (_dec - int(floor(_dec))) * 60
    minutes = int(floor(_dec))
    _dec = (_dec - int(floor(_dec))) * 60
    seconds = _dec
    fmt = "{0}\xb0"
    if minutes:
        fmt += "{1:0>2d}'"
    if seconds:
        fmt += '{2:0>2f}"'
    fmt += hemispheres[0] if dec > 0 else hemispheres[1]
    return str(fmt).format(degrees, minutes, seconds)


class XMultiSelect(MultiSelect):
    def __init__(self, ctx, req, name, eid, **kw):
        if getattr(ctx, name) and len(getattr(ctx, name)[0]):
            kw['selected'] = getattr(ctx, name)
        else:
            kw['selected'] = None
        MultiSelect.__init__(self, req, name, eid, **kw)

    def format_result(self, obj):
        o = '%s' % (getattr(obj, 'label', obj))
        return {'id': o, 'text': o}

    @classmethod
    def query(cls, name):
        return DBSession.query(getattr(amsd.models, name).name).distinct() \
                    .order_by(getattr(amsd.models, name).name)

    def get_options(self):
        return {
            'data': [self.format_result(p) for p in self.query(self.name)],
            'multiple': True}
