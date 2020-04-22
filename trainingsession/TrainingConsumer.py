import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class TrainingConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        self.channel_layer.group_add("zinnour", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard("zinnour", self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        self.send({
            "type": "message",
            "message": "pong",
        })

    def consume_msg(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
