from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('This is room_name -',self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        print('This is the group name-',self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    @database_sync_to_async
    def getuser(self,username):
        from django.contrib.auth.models import User
        return User.objects.get(username=username)

    @database_sync_to_async
    def getchatroom(self,chatroom):
        from .models import ChatRoom
        return ChatRoom.objects.get(name=chatroom)

    @database_sync_to_async
    def create_message(self, user, chatroom, message):
        from .models import Messages
        return Messages.objects.create(user=user, chatroom=chatroom, message=message)

    async def receive(self, text_data):
        # from .models import Messages
        # from django.contrib.auth.models import User
        data = json.loads(text_data)
        message = data['message']
        username = data['username']  # Ensure the username is sent from the client

        # print(message)
        # print(username)

        # Save the message to the database
        user = await self.getuser(username)
        chatroom = await self.getchatroom(self.room_name)
        await self.create_message(user,chatroom,message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username  # Send username along with the message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Include username in the event

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message
        }))
