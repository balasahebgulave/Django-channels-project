import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer


class TickTockConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        while 1:
            await asyncio.sleep(1)
            await self.send_json("tick")
            await asyncio.sleep(1)
            await self.send_json(".....tock")


class ChatConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print('------------connected---------',event)
		await self.send({
			"type":"websocket.accept"
		})

		await asyncio.sleep(2)

		await self.send({
			"type":"websocket.send",
			"text":"Hello World !"
		})

		# await self.send({
		# 	"type":"websocket.close",
		# })

	async def websocket_receive(self, event):
		print('------------received---------',event)

	async def websocket_disconnect(self, event):
		print('------------disconnected---------',event)

