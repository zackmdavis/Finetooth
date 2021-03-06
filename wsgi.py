"""
WSGI config for Finetooth project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.core.wsgi import get_wsgi_application


if os.path.exists(".development"):
    application = get_wsgi_application()
else:
    from dj_static import Cling
    application = Cling(get_wsgi_application())
