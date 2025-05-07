
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.conf import settings
from django.apps import AppConfig
from django.conf.urls.static import static
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import requests
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
django.setup()

from chat.models import Chat
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def save_chat(self, user_message, bot_response):
        Chat.objects.create(
            user_message=user_message,
            bot_response=bot_response
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        try:
            # Call Ollama API
            response = requests.post('http://0.0.0.0:11434/api/generate', 
                json={'model': 'llama2', 'prompt': message})
            bot_response = response.json()['response']
        except Exception as e:
            bot_response = f"Error: {str(e)}"

        # Save to database
        await self.save_chat(message, bot_response)

        await self.send(text_data=json.dumps({
            'user': message,
            'bot': bot_response
        }))

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/", ChatConsumer.as_asgi()),
        ])
    ),
})
