#!/usr/bin/env python

import sys
from smsgates import get_gate_class
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog [options] MESSAGE_OR_STDIN")
    parser.add_option("-g", "--gate_name", dest="gate_name",
                      help="SMS gate name")
    parser.add_option("-l", "--login", dest="login",
                      help="username/login for the SMS gate")
    parser.add_option("-p", "--password", dest="password", help="password")
    parser.add_option("-n", "--to_number", dest="to_number",
                      help="recipient phone number")

    (options, args) = parser.parse_args()

    msg = " ".join(args) if args else sys.stdin.read()

    Gate = get_gate_class(options.gate_name)
    with Gate(login=options.login, password=options.password) as gate:
        gate.send(msg, options.to_number)


if __name__ == "__main__":
    main()
