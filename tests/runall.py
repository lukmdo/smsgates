import unittest2 as unittest

# @todo: add tests for smsgates package base classes

def suite():
    """
    To run all tests:
        $ python tests/runall.py
    To run a single test:
        $ python tests/NAME_test.py
    To run code coverage:
        $ coverage run run_tests.py
        $ coverage report -m
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromName('tests.contrib_test'))
    suite.addTests(loader.loadTestsFromName('tests.vcard_contacts_test'))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
