import tempfile


DEBUG = True

SECRET_KEY = 'testing'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'markymark',
    'legaltext',
    'legaltext.tests.resources.mockapp',
)

ROOT_URLCONF = 'django.contrib.auth.urls'

SITE_ID = 1
LANGUAGES = (('en-us', 'en-us'),)

MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = '/media/'

STATIC_ROOT = tempfile.mkdtemp()
STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = []

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
