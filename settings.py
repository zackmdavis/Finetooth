"""
Django settings for Finetooth.
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

IS_DEVELOPMENT = os.path.exists('.development')

DEBUG = os.environ.get('DEBUG') or IS_DEVELOPMENT

if IS_DEVELOPMENT:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "fake_development_unsecret_key"
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'core',
)

if DEBUG and IS_DEVELOPMENT:
    INSTALLED_APPS += ('debug_toolbar',)

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

if IS_DEVELOPMENT:
    DATABASES = {
        'default': {
            # I <3 SQLite but maybe consider Postgres if/when deploying this
            # somewhere
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join('db.sqlite3'),
        }
    }
else:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

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

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = ('static',)

SERVE_STATIC_LIBS_LOCALLY = (os.environ.get('SERVE_STATIC_LIBS_LOCALLY')
                             or IS_DEVELOPMENT)

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
