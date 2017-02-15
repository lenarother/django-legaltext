import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'Django>=1.9',
    'django-markymark>=1.0.0,<1.1',
    'pytz'
]

version = '0.1'

test_requires = [
    'py>=1.4.26',
    'pyflakes==1.1.0',
    'pytest>=2.8.0',
    'pytest-cache>=1.0',
    'pytest-cov>=2.1.0',
    'pytest-flakes>=1.0.1',
    'pytest-isort==0.1.0',
    'pytest-pep8>=1.0.6',
    'pytest-django==2.9.1',
    'fake-factory==0.7.4',
    'factory-boy>=2.7.0,<2.8',
    'coverage>=4.0',
    'mock>=1.3.0',
    'pep8>=1.6.2',
    'tox',
    'tox-pyenv',
]

setup(
    name='django-legaltext',
    version=version,
    packages=find_packages(exclude=[
        'legaltext.tests',
        'legaltext.tests.factories',
        'legaltext.tests.resources',
        'legaltext.tests.tests',
    ]),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to manage legal text versions.',
    long_description=README,
    url='https://www.example.com/',
    author='Ute Brecklow, Stephan Jäkel',
    author_email='ute.brecklow@moccu.com',
    extras_require={
        'tests': test_requires,
    },
    tests_require=test_requires,
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
