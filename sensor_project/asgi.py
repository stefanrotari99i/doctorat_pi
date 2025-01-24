

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from django.urls import path
from sensor_app.consumers import SensorConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('ws/sensor/', SensorConsumer.as_asgi()),
    ]),
})
