from setuptools import setup
import smsgates


setup(
    name='smsgates',
    version=smsgates.__version__,
    license='GNU Lesser General Public License',
    url='https://github.com/ssspiochld/smsgates',
    author='lukmdo',
    author_email='me@lukmdo.com',
    description=smsgates.__about__,
    long_description=smsgates.__doc__,
    packages=['smsgates', 'smsgates.extras', 'tests'],
    scripts=['smsgates/extras/sendsms.py',
             'smsgates/extras/smsgates_bootstrap.sh'],
    test_suite='tests.runall.suite',
    zip_safe=False,
)
