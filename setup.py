import os
import sys
from setuptools import find_packages, setup


version = '1.0.0'


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
    'Django>=2',
    'django-floppyforms>=1.8',
    'django-markymark>=2.0',
]


test_requires = [
    'pytest>=5.3,<5.4',
    'pytest-cov>=2.8.1,<3',
    'pytest-django>=3.9.0,<4',
    'pytest-flakes>=4.0.0,<5',
    'pytest-isort>=0.3.1,<1',
    'pytest-pep8>=1.0.6,<2',
    'factory-boy==2.12.0,<3',
    'freezegun>=0.3.15,<1',
    'isort>=4.3.21,<4.4',
    'coverage>=4.0',
    'tox',
    'tox-pyenv',
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
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
