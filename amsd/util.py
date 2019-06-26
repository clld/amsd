# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.db.meta import DBSession
from clld.db.models.common import Contributor, Source
from clld.web.util.htmllib import HTML

import amsd.models

def contribution_detail_html(context=None, request=None, **kw):
    return {
        'data_entry': get_data_entry(context, request),
        'semantic_domains': get_sem_domains(context, request),
        'materials': get_materials(context, request),
        'techniques': get_techniques(context, request),
        'sources': get_sources(context, request),
        'source_types': get_source_types(context, request),
        'linked_filename_urls': context.get_images('web', ''),
    }

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

def get_sources(context=None, request=None, **kw):
    res = []
    if not context.source_citation:
        return ''
    for r in context.source_citation.split(';'):
        for f in DBSession.query(Source).filter(Source.pk == r):
            res.append(f.note)
    return '<ul><li>' + '</li><li>'.join(res) + '</li></ul>'

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

