"""
WSGI config for dilli_da_dhaba project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dilli_da_dhaba.settings')
application = get_wsgi_application()
