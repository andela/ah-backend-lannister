"""
WSGI config for authors project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from environment import select_env

select_env()

application = get_wsgi_application()
