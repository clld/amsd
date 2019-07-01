# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.db.meta import DBSession
from clld.db.models.common import Contributor, Source, Contribution, Contribution_files
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import get_referents, link

from math import floor
from six import text_type

from clldmpg import cdstar

import amsd.models

def contribution_detail_html(context=None, request=None, **kw):
    return {
        'data_entry': get_data_entry(context, request),
        'semantic_domains': get_sem_domains(context, request),
        'materials': get_materials(context, request),
        'techniques': get_techniques(context, request),
        'source_types': get_source_types(context, request),
        'linked_filename_urls': context.get_images(image_type='web', width='', req=request),
    }

def dataset_detail_html(context=None, request=None, **kw):
    return {
        'count_sticks': len(DBSession.query(amsd.models.MessageStick).all()),
        'count_ling_areas': len(DBSession.query(amsd.models.ling_area).all()),
        'count_motifs': len(DBSession.query(
                amsd.models.MessageStick.motifs)
                    .filter(amsd.models.MessageStick.motifs != '')
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

def get_sem_domains(context=None, request=None, **kw):
    res = []
    if not context.sem_domain:
        return ''
    for r in context.sem_domain.split(';'):
        for f in DBSession.query(amsd.models.sem_domain).filter(amsd.models.sem_domain.pk == r):
            res.append(f.name)
    return ', '.join(sorted(res))

def get_techniques(context=None, request=None, **kw):
    res = []
    if not context.technique:
        return ''
    for r in context.technique.split(';'):
        for f in DBSession.query(amsd.models.technique).filter(amsd.models.technique.pk == r):
            res.append(f.name)
    return ', '.join(sorted(res))

def get_source_types(context=None, request=None, **kw):
    res = []
    if not context.source_type:
        return ''
    for r in context.source_type.split(';'):
        for f in DBSession.query(amsd.models.source_type).filter(amsd.models.source_type.pk == r):
            res.append(f.name)
    return ', '.join(res)

def get_materials(context=None, request=None, **kw):
    res = []
    if not context.material:
        return ''
    for r in context.material.split(';'):
        for f in DBSession.query(amsd.models.material).filter(amsd.models.material.pk == r):
            res.append(f.name)
    return ', '.join(sorted(res))

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
    return text_type(fmt).format(degrees, minutes, seconds)

