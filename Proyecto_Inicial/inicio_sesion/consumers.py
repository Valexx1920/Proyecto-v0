import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MapaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Unirse a un grupo llamado "mapa"
        await self.channel_layer.group_add("mapa", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard("mapa", self.channel_name)

    # Este método será llamado desde views.py cuando alguien publique
    async def enviar_objeto(self, event):
        objeto = event['objeto']
        # Enviar mensaje JSON a todos los clientes
        await self.send(text_data=json.dumps({
            "objeto": objeto
        }))
