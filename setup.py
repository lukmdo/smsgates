from setuptools import setup
import smsgates


setup(
    name='smsgates',
    version=smsgates.__version__,
    author='ssspiochld',
    author_email='lukasz.m.dobrzanski@gmail.com',
    description=smsgates.__about__,
    long_description=smsgates.__doc__,
    packages=['smsgates', 'tests'],
    scripts=['smsgates/sendsms.py'],
    test_suite='tests.runall.suite',
    zip_safe=False
)
