import os
import vobject
from smsgates import BaseFactory
from smsgates import Contact
from smsgates import ContactBook


class ContactParserFactory(BaseFactory):
    @property
    def _choices(self):
        return {'.vcf': vcard_contactbook_parser}

    @classmethod
    def get_class(cls, name=None):
        (root, ext) = os.path.splitext(name)
        return cls()._choices[ext.lower()]


def vcard_contactbook_parser(vcard_string, cls=ContactBook,
                             contact_cls=Contact):
    contacts = filter(None,
        [vcard_contact_adapter(vcard, cls=contact_cls) for vcard in
         vobject.readComponents(vcard_string)])
    return cls(contacts)


def vcard_contact_adapter(vcard, cls=Contact):
    """Creates `cls` instance from vcard object
    :param vcard: valid vobject.vcard object
    :param cls:
    :return: cls instance or None (not enough data to build cls instance)
    """
    #    @todo: add tel_list support
    #    @todo: add groups support
    if not vcard.validate():
        raise ValueError("Input vCard must be a valid")
    if not hasattr(vcard, 'tel_list'):
        return None

    data = dict()
    data['name'] = vcard.fn.value
    data['mobile'] = next(
        (tel.value for tel in vcard.tel_list if 'CELL' in tel.TYPE_param))
    if hasattr(vcard, 'nickname'):
        data['alias'] = vcard.nickname.value

    for k in data:
        data[k] = data[k].strip()
    return cls(**data)
