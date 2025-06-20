import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AsistenciaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated and user.rol == "instructor":
            self.group_name = f"instructor_{user.id}"  # Grupo único por instructor
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def enviar_asistencia(self, event):
        await self.send(text_data=json.dumps({
            'nombre': event['nombre'],
            'fecha': event['fecha'],
            'foto': event['foto'],
            'instructor_id': event['instructor_id']
        }))

