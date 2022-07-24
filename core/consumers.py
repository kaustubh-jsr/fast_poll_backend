import json
from channels.generic.websocket import WebsocketConsumer
from .models import *
from asgiref.sync import async_to_sync,sync_to_async
from urllib.parse import parse_qs

class PollResultsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = parse_qs(self.scope["query_string"].decode("utf-8"))['poll_id'][0]
        self.room_group_name = f'poll_results_{self.room_name}'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        print('connected')
        
    def disconnect(self,close_code):
        print('disconnected')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('group discarded')
        self.close()
        
    def poll_results_update(self,event):
        print('updating poll results')
        print(event)
        self.send(text_data=json.dumps({'pollData':event.get('value')}))