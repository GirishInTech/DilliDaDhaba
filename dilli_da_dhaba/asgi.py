"""
ASGI config for dilli_da_dhaba project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dilli_da_dhaba.settings')
application = get_asgi_application()
