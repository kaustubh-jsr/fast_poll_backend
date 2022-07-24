"""
ASGI config for fast_poll_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fast_poll_backend.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket":AuthMiddlewareStack(URLRouter(
        websocket_urlpatterns
    ))
})
