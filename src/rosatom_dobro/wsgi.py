"""
WSGI config for rosatom_dobro project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rosatom_dobro.settings')

application = get_wsgi_application()
