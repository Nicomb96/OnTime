from django.urls import re_path
from .consumers import CodigoConsumer
from .consumers1 import AsistenciaConsumer

websocket_urlpatterns = [
    re_path(r'ws/codigo/$', CodigoConsumer.as_asgi()),
    re_path(r'ws/asistencia/$', AsistenciaConsumer.as_asgi()),
]
