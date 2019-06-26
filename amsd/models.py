from zope.interface import implementer

from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Language,
    Contribution,
    Contributor,
    IdNameDescriptionMixin,
    HasFilesMixin,
)

from clld.web.util.htmllib import HTML

# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class amsdLanguage(CustomModelMixin, Language):
   pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)


class ling_area(Base):
    pk = Column(Integer, primary_key=True)
    chirila_name = Column(Unicode)
    austlang_code = Column(Unicode)
    austlang_name = Column(Unicode)
    glottolog_code = Column(Unicode)


class item_type(Base, IdNameDescriptionMixin):
    pass

class material(Base, IdNameDescriptionMixin):
    pass

class data_entry(Base, IdNameDescriptionMixin):
    pass

class holder_file(Base, IdNameDescriptionMixin):
    pass

class sem_domain(Base, IdNameDescriptionMixin):
    pass

class source_type(Base, IdNameDescriptionMixin):
    pass

class technique(Base, IdNameDescriptionMixin):
    pass

class keywords(Base, IdNameDescriptionMixin):
    pass

@implementer(interfaces.IContribution)
class MessageStick(CustomModelMixin, Contribution, HasFilesMixin):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    title = Column(Unicode)
    keyword = Column(Unicode)
    obj_creator = Column(Unicode)
    date_created = Column(Unicode)
    note_place_created = Column(Unicode)
    place_created = Column(Unicode)
    item_type_pk = Column(Integer, ForeignKey("item_type.pk"))
    item_type = relationship(item_type, backref='item_type')
    ling_area_1_pk = Column(Integer, ForeignKey("ling_area.pk"))
    ling_area_2_pk = Column(Integer, ForeignKey("ling_area.pk"))
    ling_area_3_pk = Column(Integer, ForeignKey("ling_area.pk"))
    ling_area_1 = relationship('ling_area', foreign_keys=[ling_area_1_pk])
    ling_area_2 = relationship('ling_area', foreign_keys=[ling_area_2_pk])
    ling_area_3 = relationship('ling_area', foreign_keys=[ling_area_3_pk])
    notes_ling_area = Column(Unicode)
    stick_term = Column(Unicode)
    message = Column(Unicode)
    motifs = Column(Unicode)
    motif_transcription = Column(Unicode)
    sem_domain = Column(Unicode)
    dim_1 = Column(Unicode)
    dim_2 = Column(Unicode)
    dim_3 = Column(Unicode)
    material = Column(Unicode)
    technique = Column(Unicode)
    source_citation = Column(Unicode)
    source_type = Column(Unicode)
    date_collected = Column(Unicode)
    holder_file_pk = Column(Integer, ForeignKey("holder_file.pk"))
    holder_file = relationship('holder_file', foreign_keys=[holder_file_pk])
    holder_obj_id = Column(Unicode)
    collector = Column(Unicode)
    place_collected = Column(Unicode)
    creator_coyright = Column(Unicode)
    file_copyright = Column(Unicode)
    latitude = Column(
        Float(),
        CheckConstraint('-90 <= latitude and latitude <= 90'),
        doc='geographical latitude in WGS84')
    longitude = Column(
        Float(),
        CheckConstraint('-180 <= longitude and longitude <= 180 '),
        doc='geographical longitude in WGS84')
    notes_coords = Column(Unicode)
    url_institution = Column(Unicode)
    url_source_1 = Column(Unicode)
    url_source_2 = Column(Unicode)
    irn = Column(Unicode)
    notes = Column(Unicode)
    data_entry = Column(Unicode)

    def get_images(self, image_type='thumbnail', width='40'):
        if not self.files:
            return ''
        res = []
        cdstar_url = 'https://cdstar.shh.mpg.de/bitstreams/'
        for k, f in self.files.items():
            if image_type in ['web', 'thumbnail']:
                res.append(
                        HTML.a(
                            HTML.img(
                                alt = f.name,
                                title = f.name,
                                width = '%spx' % (width) if width else 'auto',
                                src = '%s/%s' % (cdstar_url, f.jsondata.get(image_type)),
                            ),
                            href = '%s/%s' % (cdstar_url, f.jsondata.get('url')),
                            target = '_new')
                        )
            else:
                res.append(HTML.img(
                    alt = f.name,
                    title = f.name,
                    src = '%s/%s' % (cdstar_url, f.jsondata.get('url')))
                )
        return '&nbsp;'.join(res)
