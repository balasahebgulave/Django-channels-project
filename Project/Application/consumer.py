import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from . models import MachineConfiguration
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async




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
		print('------------received---------',json.loads(event['text']))



	async def websocket_disconnect(self, event):
		print('------------disconnected---------',event)



class AddMachineConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print('---------connected AddMachineConsumer---------',event)
		await self.send({
			"type":"websocket.accept"
		})

		

	async def websocket_receive(self, event):
		print('---------received AddMachineConsumer---------',event)
		
		try:
			machinedetails = json.loads(event['text'])
			try:
				check_exist = await self.check_machine(machinedetails)
			except:
				check_exist = None

			if check_exist == None:
				await self.save_machine(machinedetails)
				response = "Machine Saved Successfully"
			else:
				response = f"Machine allredy present in team : {check_exist.team}"

			await self.send({
				"type":"websocket.send",
				"text": response
			})

		except Exception as e:
			await self.send({
				"type":"websocket.send",
				"text":f"Error while adding machine : {str(e)}"
			})
			

	async def websocket_disconnect(self, event):
		print('---------disconnected AddMachineConsumer---------',event)


	@database_sync_to_async
	def save_machine(self, machinedetails):
		machine_object = MachineConfiguration(team = machinedetails['team'], machine_ip = machinedetails['machineip'],
			adminuser = machinedetails['machineuser'], password = machinedetails['machinepassword'])
		machine_object.save()
		return True

	@database_sync_to_async
	def check_machine(self, machinedetails):
		machine_object = MachineConfiguration.objects.get(machine_ip=machinedetails['machineip'])
		return machine_object

	


	


class DisplayAllMachine(AsyncConsumer):
	async def websocket_connect(self, event):
		print('----------ShowallMachine--connected---------',event)
		await self.send({
			"type":"websocket.accept"
		})

	async def websocket_receive(self, event):
		print('----------ShowallMachine--received---------',json.loads(event['text']))
		team = json.loads(event['text'])['team']
		try:
			teamwise_machine_object = await self.show_teamwise_machine(team)
		except Exception as e:
			teamwise_machine_object = str(e)

		await self.send({
				"type":"websocket.send",
				"text": json.dumps(teamwise_machine_object)
		})


	async def websocket_disconnect(self, event):
		print('----------ShowallMachine--disconnected---------',event)

	@database_sync_to_async
	def show_teamwise_machine(self, team):
		teamwise_machine_object = MachineConfiguration.objects.filter(team=team)
		teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, i.password) for i in teamwise_machine_object]
		return teamwise_machine_object
