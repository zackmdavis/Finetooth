"""
Django settings for Finetooth.
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# TODO: review
# https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# XXX TODO FIXME DANGER: the security warning on the previous line is
# big deal; if/when deploying this somewhere, change this and DO NOT
# keep the real value in a publicly-visible Git repo
SECRET_KEY = "fake_development_unsecret_key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'debug_toolbar',
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        # I <3 SQLite but maybe consider Postgres if/when deploying this
        # somewhere
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('db.sqlite3'),
    }
}

AUTH_USER_MODEL = "core.FinetoothUser"

AUTH_REDIRECT_URL = "/"

if DEBUG:
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TEMPLATE_DIRS = ('templates',)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'core.context_processors.tag_cloud_context_processor',
    'core.context_processors.contextual_static_serving_context_processor'
)

STATICFILES_DIRS = ('static',)
SERVE_STATIC_LIBS_LOCALLY = True

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

POSTS_PER_PAGE = 15
