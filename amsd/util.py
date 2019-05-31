# coding: utf8
from __future__ import unicode_literals, print_function, division

from clld.db.meta import DBSession
from clld.db.models.common import Contributor
from clld.web.util.htmllib import HTML

import amsd.models

def contribution_detail_html(context=None, request=None, **kw):
    return {
        'data_entry': get_data_entry(context, request),
        'linked_filename_urls': get_linked_filename_urls(context.linked_filenames, 'web', '')
    }

def get_data_entry(context=None, request=None, **kw):
    res = []
    if not context.data_entry:
        return None
    for r in context.data_entry.split(';'):
        for f in DBSession.query(Contributor).filter(Contributor.id == r):
            res.append(HTML.a(f.name, href='%s/%s' % (request.route_url('contributors'), r)))
    return ', '.join(res)

def get_linked_filename_urls(pks, image_type='thumbnail', width='40'):
    if not pks:
        return ''
    res = []
    cdstar_url = 'https://cdstar.shh.mpg.de/bitstreams/'
    for r in pks.split(';'):
        for f in DBSession.query(amsd.models.linked_filenames).filter(amsd.models.linked_filenames.pk == r):
            s = '%s%s/' % (cdstar_url, f.oid)
            if image_type in ['web', 'thumbnail']:
                if f.name not in ['00-Text_reference.png', '00-No_image_available.png']:
                    if f.path.lower().endswith('pdf'):
                        if width == '' or not width:
                            w = '180'
                        else:
                            w = width
                        res.append(
                            HTML.a(
                                HTML.img(title=f.name, width='%spx' % (w),
                                            src='%sEAEA0-52CC-0295-6B71-0/00_Text_reference.png' % (cdstar_url))
                                , href='%s%s' % (s, f.path), target='_new')
                            )
                    else:
                        res.append(
                            HTML.a(
                                HTML.img(title=f.name, width='%spx' % (width),
                                            src='%s%s.jpg' % (s, image_type))
                                , href='%s%s' % (s, f.path), target='_new')
                            )
            else:
                res.append(HTML.img(title=f.name, src='%s%s' % (s, f.path)))
    return '&nbsp;'.join(res)
