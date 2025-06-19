import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ontime_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ontime.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ontime_app.routing.websocket_urlpatterns
        )
    ),
})
