from __future__ import unicode_literals
import sys
import re
from collections import OrderedDict

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.path import Path
from clldutils.dsv import reader
from clldutils.misc import slug

import amsd
from amsd import models

data_file_path = Path(amsd.__file__).parent / '../..' / 'amsd-data'

def dicts(name):
    res = []
    for item in reader(data_file_path / 'raw/{0}.csv'.format(name), dicts=True):
        res.append(item)
    return res

def main(args):

    data = Data()

    dataset = common.Dataset(
        id=amsd.__name__,
        name="AMSD",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='amsd.clld.org',
        contact='kelly@shh.mpg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    editors = OrderedDict([('Piers Kelly', None)])

    # data_entry => Contributor
    for row in sorted(dicts('data_entry'), key=lambda x: [
                x['name'].lower()] ):
        if row['name'] in editors:
            editors[row['name']] = row['pk']
        data.add(
            common.Contributor,
            row['pk'],
            id=row['pk'],
            name=row['name']
        )

    for i, cid in enumerate(editors.values()):
        common.Editor(dataset=dataset, contributor=data['Contributor'][cid], ord=i + 1)

    for row in dicts('source_citation'):
        data.add(
            common.Source,
            row['pk'],
            id=row['pk'],
            note=row['name']
        )

    for row in dicts('ling_area'):
        data.add(
            models.ling_area,
            row['pk'],
            chirila_name = row['chirila_name'],
            austlang_code = row['austlang_code'],
            austlang_name = row['austlang_name'],
            glottolog_code = row['glottolog_code'],
        )

    for row in dicts('item_type'):
        data.add(
            models.item_type,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('technique'):
        data.add(
            models.technique,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('keywords'):
        data.add(
            models.keyword,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('material'):
        data.add(
            models.material,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('source_type'):
        data.add(
            models.source_type,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('sem_domain'):
        data.add(
            models.sem_domain,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('holder_file'):
        data.add(
            models.holder_file,
            row['pk'],
            name = row['name'],
        )

    for row in dicts('linked_filenames'):
        data.add(
            models.linked_filenames,
            row['pk'],
            name = row['name'],
            oid = row['oid'],
            path = row['path'],
        )

    # sticks => MessageStick
    for i, row in enumerate(dicts('sticks')):
        data.add(
            models.MessageStick,
            row['pk'],
            id = row['amsd_id'].replace('.', '_') or "amsd_{:05d}".format(i),
            title = row['title'],
            keywords = row['keywords'],
            description = row['description'],
            obj_creator = row['obj_creator'],
            date_created = row['date_created'],
            note_place_created = row['note_place_created'],
            place_created = row['place_created'],
            item_type_pk = row['item_type'] or None,
            ling_area_1_pk = row['ling_area_1'] or None,
            ling_area_2_pk = row['ling_area_2'] or None,
            ling_area_3_pk = row['ling_area_3'] or None,
            notes_ling_area = row['notes_ling_area'],
            stick_term = row['stick_term'],
            message = row['message'],
            motifs = row['motifs'],
            motif_transcription = row['motif_transcription'],
            sem_domain = row['sem_domain'],
            dim_1 = row['dim_1'],
            dim_2 = row['dim_2'],
            dim_3 = row['dim_3'],
            material = row['material'],
            technique = row['technique'],
            source_citation = row['source_citation'],
            source_type = row['source_type'] or None,
            date_collected = row['date_collected'],
            holder_file_pk = row['holder_file'] or None,
            holder_obj_id = row['holder_obj_id'],
            collector = row['collector'],
            place_collected = row['place_collected'],
            creator_coyright = row['creator_coyright'],
            file_copyright = row['file_copyright'],
            latitude = row['lat'] or None,
            longitude = row['long'] or None,
            notes_coords = row['notes_coords'],
            url_institution = row['url_institution'],
            url_source_1 = row['url_source_1'],
            url_source_2 = row['url_source_2'],
            irn = row['irn'],
            notes = row['notes'],
            data_entry = row['data_entry'],
            linked_filenames = row['linked_filenames'],
        )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
