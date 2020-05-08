import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TrainingConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.scope['url_route']['kwargs']['session_name'], self.channel_name)
        print(self.scope['url_route']['kwargs']['session_name'])
        self.accept()


    def training_session_message(self, event):
        self.send(text_data=event["data"])

