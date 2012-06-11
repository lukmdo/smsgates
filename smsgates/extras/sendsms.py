#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
import smsgates
from smsgates import ContactBook
from smsgates.extras import ContactParserFactory


USER_HOMEDIR = os.path.expanduser('~')
CONTACT_BOOK_DEFAULT = os.path.join(USER_HOMEDIR, 'Documents', 'contacts.vcf')


def main():
    parser = argparse.ArgumentParser(usage="""
    %(prog)s CONTACT MSG
    %(prog)s [options]""")

    parser.add_argument("--version", action='version',
                        version=smsgates.__version__)
    parser.add_argument("-v", "--verbose", action='count',
                        help="show verbose output")
    parser.add_argument("-g", "--gate_name", help="SMS gate name")
    parser.add_argument("-l", "--login", help="username for the SMS gate")
    parser.add_argument("-p", "--password", help="password")
    parser.add_argument("-m", "--message", nargs='*', help="message to send")
    parser.add_argument("-t", "--to_contact",
                        help="recipient alias from the contacts_file")
    parser.add_argument("-n", "--to_number", help="recipient phone number")
    parser.add_argument("-c", "--contacts_file", default=CONTACT_BOOK_DEFAULT,
                        type=argparse.FileType(),
                        help="vCard contacts file (default loc: %(default)s)")
    parser.add_argument("-s", "--show_contacts", nargs='?', const=True,
                        help="lists contacts from CONTACT_FILE")

    args, extra_args = parser.parse_known_args()
    if len(sys.argv) == 1:
        parser.print_usage()
        return

    contacts_book = ContactBook(from_file=args.contacts_file,
                                factory=ContactParserFactory)
    if args.show_contacts:
        if args.show_contacts != True:
            # assume utf8 input otherwise: 
            # ```UnicodeDecodeError: 'ascii' codec can't decode...```
            to = unicode(args.show_contacts, 'utf8')  
            contacts = set.union(
                contacts_book.search(alias__ilike=to),
                contacts_book.search(fullname__ilike=to))
        else:
            contacts = list(contacts_book)
        map(print, sorted(contacts, key=lambda c: c.alias))
        return

    for arg_name in ['login', 'password', 'gate_name']:
        if not getattr(args, arg_name):
            parser.error("argument %s is required to send message" % arg_name)

    from smsgates.contrib import GateFactory
    GateClass = GateFactory.get_class(args.gate_name)
    with GateClass(verbose=args.verbose, login=args.login,
                   password=args.password) as gate:
        if args.message:
            msg = " ".join(args.message)
        else:
            msg = " ".join(extra_args) or sys.stdin.read()

        if args.to_number:
            contacts = [args.to_number]
        else:
            to = args.to_contact if args.to_contact else extra_args.pop(0)
            # assume utf8 input otherwise: 
            # ```UnicodeDecodeError: 'ascii' codec can't decode...```
            to = unicode(to, 'utf8')  
            contacts = set.union(
                contacts_book.search(alias__ilike=to),
                contacts_book.search(fullname__ilike=to))

        gate.send(msg, *contacts)


if __name__ == "__main__":
    main()
