import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


version = '0.0.1'


install_requires = [
    'Django>=1.9',
    'django-markymark>=1.0.0',
    'pytz'
]


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
    'freezegun>=0.3.7,<0.4',
    'coverage>=4.0',
    'mock>=1.3.0',
    'pep8>=1.6.2',
    'tox',
    'tox-pyenv',
]

setup(
    name='django-legaltext',
    version=version,
    description=(
        'django-legaltext helps to manage participation and privacy legal terms in forms.'),
    keywords=['legaltext', 'django'],
    packages=find_packages(exclude=[
        'testing',
        'testing.tests',
        'testing.tests.legaltext',
        'testing.tests.mockapp',
        'testing.factories',
        'examples',
        'examples.mockapp',
        'examples.mockapp.migrations'
    ]),
    include_package_data=True,
    license='Apache License (2.0)',
    long_description='README.rst',
    url='https://github.com/moccu/django-legaltext/',
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    extras_require={
        'tests': test_requires,
    },
    install_requires=install_requires,
    tests_require=test_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
