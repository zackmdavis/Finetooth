"""
Django settings for Finetooth.
"""

import os
from enum import Enum

from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

Environment = Enum('Environment', ("development", "heroku_demo",
                                   # unused as yet---
                                   "production"))

# XXX: surely there must be a better way to detect deployment
# environment at runtime?
ENVIRONMENT = (Environment.development if os.path.exists('.development')
               else Environment.heroku_demo)

DEBUG = os.environ.get('DEBUG') or ENVIRONMENT is Environment.development

if ENVIRONMENT is Environment.development:
    SECRET_KEY = (os.environ.get('SECRET_KEY')
                  or "fake_development_unsecret_key")
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'core',
)

if (DEBUG and ENVIRONMENT is Environment.development and
    not os.path.exists(".disable_debug_toolbar")):
    INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.FinetoothEnvironmentMiddleware'
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

if ENVIRONMENT is Environment.development:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join('db.sqlite3'),
        }
    }
else:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

AUTH_USER_MODEL = "core.FinetoothUser"

AUTH_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

if DEBUG and ENVIRONMENT is Environment.development:
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = (
  ('en', _('English')),
#  ('es', _('Spanish')),
)

LOCALE_PATHS = ('translations',)

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ('templates',),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.tag_cloud_context_processor',
                ('core.context_processors'
                 '.contextual_static_serving_context_processor'),
                'core.context_processors.sidebar_login_form_context_processor',
                'core.context_processors.monthly_archives_context_processor',
            ),
        },
    },
)

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = ('static',)

SERVE_STATIC_LIBS_LOCALLY = (ENVIRONMENT is Environment.development and
                             not os.environ.get('NONLOCAL_STATIC_LIBS'))

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'log_format': {
            'format' : ("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] "
                        "%(message)s")
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1 * (1024)**2,  # 1 MiB
            'backupCount': 3,
            'filename': 'logs/finetooth.log',
            'formatter': 'log_format'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
        },
        'core': {
            'handlers': ['file'],
            'propogate': True,
            'level': 'INFO',
        },
    }
}

TEST_RUNNER = 'concerned_testrunner.ConcernedTestRunner'

POSTS_PER_PAGE = 15
