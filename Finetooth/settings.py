"""
Django settings for Finetooth.
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# TODO: review
# https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# XXX TODO FIXME DANGER: the security warning on the previous line is
# big deal; if/when deploying this somewhere, change this and DO NOT
# keep the real value in a publicly-visible Git repo
SECRET_KEY = '4y+opi-^iz@s+(#io3b2l1+w89c44vos%9npcxap8=#+4c11!n'

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
    'south',
    'Finetooth.core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Finetooth.urls'

WSGI_APPLICATION = 'Finetooth.wsgi.application'

DATABASES = {
    'default': {
        # I <3 SQLite but maybe consider Postgres if/when deploying this
        # somewhere
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = os.path.join(BASE_DIR, "Finetooth", "templates")

STATIC_URL = '/static/'
