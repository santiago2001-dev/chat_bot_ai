from django.urls import re_path
from .consumers import ProductConsumer

websocket_urlpatterns = [
    re_path(r'ws/products/$', ProductConsumer.as_asgi()),
]
