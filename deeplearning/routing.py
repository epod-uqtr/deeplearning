from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from django.urls import path

from trainingsession.TrainingConsumer import TrainingConsumer

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        URLRouter([
            path('trainingsession/<str:session_name>/', TrainingConsumer),
            #url(r"^trainingsession/$", TrainingConsumer),

        ])
    )
})
