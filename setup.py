import os
import sys
from setuptools import find_packages, setup


version = '0.3.0'


# TEMPORARY FIX FOR
# https://bitbucket.org/pypa/setuptools/issues/450/egg_info-command-is-very-slow-if-there-are
TO_OMIT = ['.git', '.tox']
orig_os_walk = os.walk

def patched_os_walk(path, *args, **kwargs):
    for (dirpath, dirnames, filenames) in orig_os_walk(path, *args, **kwargs):
        if '.git' in dirnames:
            # We're probably in our own root directory.
            print("MONKEY PATCH: omitting a few directories like .git and .tox...")
            dirnames[:] = list(set(dirnames) - set(TO_OMIT))
        yield (dirpath, dirnames, filenames)

os.walk = patched_os_walk
# END IF TEMPORARY FIX.


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


install_requires = [
    'Django>=1.11.23,<2.0',
    'django-floppyforms>=1.7.0',
    'django-markymark>=1.0.0',
]


test_requires = [
    'py>=1.4.26',
    'pyflakes==2.1.1',
    'pytest>=3.0.7',
    'pytest-cache>=1.0',
    'pytest-cov>=2.1.0',
    'pytest-flakes>=4.0.0',
    'pytest-isort==0.1.0',
    'pytest-pep8>=1.0.6',
    'pytest-django==3.5.0',
    'fake-factory==0.7.4',
    'factory-boy>=2.7.0,<2.8',
    'freezegun>=0.3.7,<0.4',
    'coverage>=4.0',
    'mock>=1.3.0',
    'pep8>=1.6.2',
    'tox',
    'tox-pyenv',
    'isort==4.2.5'
]

setup(
    name='django-legaltext',
    description='django-legaltext helps to manage legal text versioning.',
    version=version,
    keywords=['legaltext', 'django'],
    packages=find_packages(exclude=[
        'testing*',
        'examples*',
    ]),
    include_package_data=True,
    license='BSD',
    long_description=README,
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
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
