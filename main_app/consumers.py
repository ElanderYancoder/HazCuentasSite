import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"user_{self.scope['user'].id}"

        if self.scope['user'].is_authenticated:
            # Unirse al grupo del usuario
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Salir del grupo del usuario
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Opcional: Manejar mensajes enviados por el cliente
        pass

    async def send_notification(self, event):
        # Enviar la notificación al cliente
        await self.send(text_data=json.dumps({
            'title': event['title'],
            'message': event['message']
        }))
