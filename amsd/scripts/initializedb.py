import sys
import re
import mimetypes
from collections import OrderedDict

from clld.cliutil import Data
from clld.db import fts
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.path import Path
from csvw.dsv import reader
from clldutils.misc import slug, nfilter

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
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="https://creativecommons.org/licenses/by/4.0/",
        domain='amsd.clld.org',
        contact='piers.kelly@gmail.com',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    editors = OrderedDict([('Piers Kelly', None), ('Junran Lei', None),
                           ('Hans-Jörg Bibiko', None), ('Lorina Barker', None)])

    # data_entry => Contributor
    dataentry_map = {}
    dict_dataentry = dicts('data_entry')
    dict_dataentry.append(OrderedDict([('pk', str(len(dict_dataentry)+1)),
                                       ('name', 'Junran Lei')]))
    dict_dataentry.append(OrderedDict([('pk', str(len(dict_dataentry)+1)),
                                       ('name', 'Hans-Jörg Bibiko')]))
    for row in sorted(dict_dataentry, key=lambda x: [x['name'].lower()]):
        if row['name'] in editors:
            editors[row['name']] = row['pk']
        d = data.add(
            common.Contributor,
            row['pk'],
            id=row['pk'],
            name=row['name']
        )
        dataentry_map[row['pk']] = d

    for i, cid in enumerate(editors.values()):
        common.Editor(dataset=dataset, contributor=data['Contributor'][cid], ord=i + 1)

    for row in dicts('source_citation'):
        data.add(
            common.Source,
            row['pk'],
            id=row['pk'],
            note=row['name'],
            name=row['name'],
        )

    for row in dicts('ling_area'):
        data.add(
            models.ling_area,
            row['pk'],
            chirila_name=row['chirila_name'],
            austlang_code=row['austlang_code'],
            austlang_name=row['austlang_name'],
            glottolog_code=row['glottolog_code'],
        )
    fd = {}
    for row in dicts('linked_filenames'):
        if row['name'] not in ['00-Text_reference.png', '00-No_image_available.png']:
            fd[row['pk']] = dict(
                name=row['name'],
                oid=row['oid'],
                path=row['path'],
                mimetype=mimetypes.guess_type(row['path'])[0] if row['path'] else None,
            )

    glossed_artefact_id = None
    interpreted_artefact_id = None

    for m in 'item_type technique keywords material source_type '\
            'sem_domain holder_file item_subtype cultural_region'.split():
        for row in dicts(m):
            data.add(
                getattr(models, m),
                row['pk'],
                name=row['name'],
            )
            if m == 'keywords':
                if glossed_artefact_id is None and 'glossed_artefact' == row['name']:
                    glossed_artefact_id = int(row['pk'])
                if interpreted_artefact_id is None and 'interpreted_artefact' == row['name']:
                    interpreted_artefact_id = int(row['pk'])

    DBSession.flush()

    # sticks => MessageStick
    no_fts_cols = ['pk', 'latitude', 'longitude', 'item_type',
                   'irn', 'data_entry', 'dim_1', 'dim_2', 'dim_3', 'data_entry',
                   'ling_area_1', 'ling_area_2', 'ling_area_3', 'holder_file']
    x_cols = ['sem_domain', 'material', 'source_type', 'technique', 'keywords',
              'holder_file', 'item_type', 'item_subtype', 'cultural_region']
    for i, row in enumerate(dicts('sticks')):

        fts_items = []
        for col in row.keys():
            if col:
                if col == 'amsd_id':
                    fts_items.append(row['amsd_id'].replace('.', '_') or "amsd_{:05d}".format(i),)
                elif col not in no_fts_cols and not col.endswith('_pk'):
                    fts_items.append(row[col])

        for t in x_cols:
            if row[t]:
                for _, k in enumerate(row[t].split(';')):
                    fts_items.append(str(data[t][k]))
                    fts_items.extend(str(data[t][k]).split('_'))

        for t in ['ling_area_1', 'ling_area_2', 'ling_area_3']:
            if row[t]:
                for _, k in enumerate(row[t].split(';')):
                    fts_items.append(data['ling_area'][k].chirila_name)
                    fts_items.append(data['ling_area'][k].austlang_code)
                    fts_items.append(data['ling_area'][k].austlang_name)
                    fts_items.append(data['ling_area'][k].glottolog_code)

        if row['source_citation']:
            for k in row['source_citation'].split(';'):
                data.add(
                    common.ContributionReference,
                    k,
                    contribution_pk=int(row['pk']),
                    source_pk=int(k),
                )
                fts_items.append(str(data['Source'][k]))

        if row['linked_filenames']:
            for j, k in enumerate(row['linked_filenames'].split(';')):
                if k in fd:
                    oid = fd[k].get('oid')
                    mt = fd[k].get('mimetype')
                    refobjid = ''
                    if mt == 'application/pdf':
                        refobjid = oid
                        # use for web, thumbnail a place holder image
                        oid = 'EAEA0-52CC-0295-6B71-0'
                    n = fd[k].get('name')
                    data.add(
                        common.Contribution_files,
                        k,
                        id='%s-%s-%i' % (k, row['pk'], j),
                        object_pk=int(row['pk']),
                        name=n,
                        jsondata=dict(
                            original=fd[k].get('path'),
                            objid=oid,
                            refobjid=refobjid,
                            web='web.jpg',
                            thumbnail='thumbnail.jpg',
                        ),
                        ord=j,
                        mime_type=mt,
                    )
                    fts_items.append(n)
                    fts_items.extend(nfilter(re.split(r'[_\-\.]', n)))

        ms = data.add(
            models.MessageStick,
            row['pk'],
            id=row['amsd_id'].replace('.', '_') or "amsd_{:05d}".format(i),
            title=row['title'],
            description=row['description'],
            obj_creator=row['obj_creator'],
            date_created=row['date_created'],
            note_place_created=row['note_place_created'],
            place_created=row['place_created'],
            item_type_pk=row['item_type'] or None,
            item_subtype_pk=row['item_subtype'] or None,
            state_territory=row['state_territory'],
            cultural_region_pk=row['cultural_region'] or None,
            ling_area_1_pk=row['ling_area_1'] or None,
            ling_area_2_pk=row['ling_area_2'] or None,
            ling_area_3_pk=row['ling_area_3'] or None,
            notes_ling_area=row['notes_ling_area'],
            stick_term=row['stick_term'],
            message=row['message'],
            motifs=row['motifs'],
            motif_transcription=row['motif_transcription'],
            dim_1=row['dim_1'],
            dim_2=row['dim_2'],
            dim_3=row['dim_3'],
            date_collected=row['date_collected'],
            holder_file_pk=row['holder_file'] or None,
            holder_obj_id=row['holder_obj_id'],
            collector=row['collector'],
            place_collected=row['place_collected'],
            creator_copyright=row['creator_copyright'],
            file_copyright=row['file_copyright'],
            latitude=row['lat'] or None,
            longitude=row['long'] or None,
            notes_coords=row['notes_coords'],
            url_institution=row['url_institution'],
            url_source_1=row['url_source_1'],
            url_source_2=row['url_source_2'],
            irn=row['irn'],
            notes=row['notes'],
            data_entry=row['data_entry'],
            related_entries=row['related_entries'],
            fts=fts.tsvector('\n'.join(re.sub(r'[_\-]', '.', v) for v in fts_items if v)),
            jsondata={'color': '#000000'},
        )

        DBSession.flush()
        for c in row['data_entry'].split(';'):
            if c:
                DBSession.add(common.ContributionContributor(
                    contribution=ms,
                    contributor=dataentry_map[c],
                    ord=1,
                    primary=True))

    has_glossed_artefact = set()
    has_interpreted_artefact = set()

    for row in dicts('sticks'):
        for t in ['sem_domain', 'material', 'source_type', 'technique', 'keywords']:
            if row[t]:
                for _, k in enumerate(row[t].split(';')):
                    if t == 'keywords':
                        if int(k) == glossed_artefact_id:
                            has_glossed_artefact.add(int(row['pk']))
                        if int(k) == interpreted_artefact_id:
                            has_interpreted_artefact.add(int(row['pk']))
                    data.add(
                        getattr(models, 'x_%s' % (t)),
                        k,
                        object_pk=int(row['pk']),
                        item_pk=int(k),
                    )

    for row in DBSession.query(models.MessageStick):
        if row.pk in has_glossed_artefact:
            row.jsondata = {'color': '#fdfd53'}
        if row.pk in has_interpreted_artefact and row.pk not in has_glossed_artefact:
            row.jsondata = {'color': '#bc271a'}


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
