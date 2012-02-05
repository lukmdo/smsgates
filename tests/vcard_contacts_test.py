import textwrap
from collections import namedtuple
import unittest2 as unittest
import vobject
from smsgates import Contact
from smsgates.extras import vcard_contactbook_parser
from smsgates.extras import vcard_contact_adapter


class VCardTest(unittest.TestCase):
    def setUp(self):
        vcard_data = dict(
            nickname=u'x',
            mobile=u'3333308',
            name=u'NAME SURNAME',
            firstname=u'NAME',
            surname=u'SURNAME',
            email=u'x@X.com')
        self.vcard_data = namedtuple('Contact', vcard_data.keys())(
            **vcard_data)
        self.contact = Contact(alias=self.vcard_data.nickname,
                               mobile=self.vcard_data.mobile,
                               name=self.vcard_data.name)
        vcard_str = """
        BEGIN:VCARD
        VERSION:3.0
        FN:{name}
        N:{surname};{firstname};;;
        NICKNAME:{nickname}
        EMAIL;TYPE=INTERNET:{email}
        TEL;TYPE=CELL:{mobile}
        END:VCARD
        """.format(
            name=self.vcard_data.name,
            firstname=self.vcard_data.firstname,
            surname=self.vcard_data.surname,
            nickname=self.vcard_data.nickname,
            email=self.vcard_data.email,
            mobile=self.vcard_data.mobile)
        self.vcard_str = textwrap.dedent(vcard_str)
        self.vcard = vobject.readOne(self.vcard_str)

    def test_vcard_contactbook(self):
        contactbook = vcard_contactbook_parser(self.vcard_str)
        self.assertEqual(1, len(contactbook))
        self.assertIn(self.contact, contactbook)

    def test_vcard_contact_adapter(self):
        contact = vcard_contact_adapter(self.vcard)
        self.assertEqual(self.contact, contact)
        self.contact.new_prop = "VALUE"
        self.assertNotEqual(self.contact, contact)

if __name__ == '__main__':
    unittest.main()
