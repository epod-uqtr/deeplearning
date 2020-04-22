from channels.generic.websocket import AsyncWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from trainingsession.TrainingConsumer import TrainingConsumer

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        URLRouter([
            url(r"^trainingsession/$", TrainingConsumer),
        ])
    )
})
