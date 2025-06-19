from django.urls import re_path
from .consumers import CodigoConsumer

websocket_urlpatterns = [
    re_path(r'ws/codigo/$', CodigoConsumer.as_asgi()),
]
