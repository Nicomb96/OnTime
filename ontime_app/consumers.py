import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CodigoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        await self.channel_layer.group_add('codigo', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('codigo', self.channel_name)

    async def enviar_codigo(self, event):
        await self.send(text_data=json.dumps({
            'codigo': event['codigo'],
            'qr': event.get('qr', '')
        }))
