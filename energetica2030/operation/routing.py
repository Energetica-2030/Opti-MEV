from django.urls import re_path
from .consumers import mapConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', mapConsumer.as_asgi())
]