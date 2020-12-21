import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer
import json, datetime, random,time
from . models import MachineConfiguration, CreateTaskProfile, UserSeed
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User 
from concurrent.futures import ThreadPoolExecutor


from django.dispatch import receiver
from django.db.models.signals import post_save
from . models import MachineConfiguration

@receiver(post_save, sender=MachineConfiguration)
def check_signals(sender, **kwargs):
	instance = kwargs.get('instance', None)
	print('----------post_save signal instance----------',kwargs)
	print('----------post_save signal called----------',kwargs.get('created', False))


def get_current_user(session_key):
	session = Session.objects.get(session_key=session_key)
	session_data = session.get_decoded()
	uid = session_data.get('_auth_user_id')
	user = User.objects.get(id=uid)
	return user



class CpuRamConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		await self.accept()
		# print('-------',self.scope['session']['team'])
		while 1:
			total_machines, active_machines, teamwise_machine_object = await self.get_live_machine_conf(self.scope['session']['team'])
			live_data = {'data':teamwise_machine_object, 'total_machines':total_machines, 'active_machines':active_machines}
			await asyncio.sleep(1)
			await self.send_json(live_data)

	@database_sync_to_async
	def get_live_machine_conf(self, team):
		teamwise_machine_object_old = MachineConfiguration.objects.filter(team=team)
		time.sleep(1)
		teamwise_machine_object_current = MachineConfiguration.objects.filter(team=team)
		total_machines = teamwise_machine_object_current.count()
		active_machines = len([i for i in teamwise_machine_object_current if i.cpu_usage != 'Not Active'])
		teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, i.password, i.cpu_usage, i.ram_usage, i.disk_usage) for i in teamwise_machine_object_current]
		
		for old,current in zip(teamwise_machine_object_old,teamwise_machine_object_current):
			if old.cpu_usage == current.cpu_usage:
				current.cpu_usage = "Not Active"
				current.ram_usage = "Not Active"
				current.disk_usage = "Not Active"
				current.save()
		return total_machines, active_machines, teamwise_machine_object


class ChatConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

		await asyncio.sleep(2)

		await self.send({
			"type":"websocket.send",
			"text":"Hello World !"
		})

		

	async def websocket_receive(self, event):
		print('------------received---------',json.loads(event['text']))
		nsm_data = json.loads(event['text'])
		await self.save_nsm_data(nsm_data)

	@database_sync_to_async
	def save_nsm_data(self, nsm_data):
		objs = MachineConfiguration.objects.filter(machine_ip=nsm_data["machineip"])
		for obj in objs:
			obj.cpu_usage = nsm_data['cpu_usage']
			obj.ram_usage = nsm_data['ram_usage']
			obj.disk_usage = nsm_data['disk_usage']
			obj.save()

		return True

	async def websocket_disconnect(self, event):
		print('------------disconnect---------',event)



class AddMachineConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

	async def websocket_receive(self, event):
		machinedetails = json.loads(event['text'])

		if 'deletemachine' in machinedetails.keys():
				machine_object = await self.delete_machine(machinedetails['deletemachine'])
				team = machine_object.team
				machine_object.delete()
				uniqueteam = await self.show_unique_team()
				try:
					teamwise_machine_object = await self.show_teamwise_machine(team)
				except Exception as e:
					teamwise_machine_object = str(e)


				await self.send({
						"type":"websocket.send",
						"text": json.dumps({'response':"Machine Deleted Successfully",'uniqueteam':uniqueteam,'teamwise_machine':teamwise_machine_object})				
				})
		else:

			try:
				check_exist = await self.check_machine(machinedetails)
			except:
				check_exist = None
			if check_exist == None:
				await self.save_machine(machinedetails)
				response = "Machine Saved Successfully"
			else:
				response = f"Machine allredy present in team : {check_exist.team}"
			uniqueteam = await self.show_unique_team()

			await self.send({
				"type":"websocket.send",
				"text": json.dumps({'response':response,'uniqueteam':uniqueteam})
			})
	

	@database_sync_to_async
	def show_teamwise_machine(self, team):
		try:
			teamwise_machine_object = MachineConfiguration.objects.filter(team=team)
			teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, i.password, i.cpu_usage, i.ram_usage, i.disk_usage) for i in teamwise_machine_object]
		except:
			teamwise_machine_object = ''

		return teamwise_machine_object

			
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

	@database_sync_to_async
	def show_unique_team(self):
		teams = MachineConfiguration.objects.values('team').distinct()
		uniqueteam = []
		for i,j in enumerate(teams):
			uniqueteam.append((i+1,j))
		return uniqueteam

	@database_sync_to_async
	def delete_machine(self, machine_id):
		machine_object = MachineConfiguration.objects.get(id=machine_id)
		return machine_object

	async def websocket_disconnect(self, event):
		print('------------AddMachineConsumer---------',event)



class DisplayAllMachineConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

		uniqueteam = await self.show_unique_team()
		await self.send({
			"type":"websocket.send",
			"text":json.dumps({'uniqueteam':uniqueteam})
		})

	async def websocket_receive(self, event):
		machinedetails = json.loads(event['text'])
		if 'team' in machinedetails.keys():
			try:
				teamwise_machine_object = await self.show_teamwise_machine(machinedetails['team'])
			except Exception as e:
				teamwise_machine_object = str(e)

			await self.send({
					"type":"websocket.send",
					"text": json.dumps({'teamwise_machine':teamwise_machine_object})
			})
	
	@database_sync_to_async
	def show_teamwise_machine(self, team):
		teamwise_machine_object = MachineConfiguration.objects.filter(team=team)
		teamwise_machine_object = [(i.id, i.team, i.machine_ip, i.adminuser, i.password, i.cpu_usage, i.ram_usage, i.disk_usage) for i in teamwise_machine_object]
		return teamwise_machine_object

	@database_sync_to_async
	def show_unique_team(self):
		teams = MachineConfiguration.objects.values('team').distinct()
		uniqueteam = []
		for i,j in enumerate(teams):
			uniqueteam.append((i+1,j))
		return uniqueteam


	async def websocket_disconnect(self, event):
		print('------------DisplayAllMachineConsumer---------',event)


class CreateTaskProfileConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})
		usertaskprofiles = await self.user_task_profile()
		await self.send({
				"type":"websocket.send",
				"text": json.dumps({'usertaskprofiles':usertaskprofiles})
		})

	async def websocket_receive(self, event):
		profiledata = json.loads(event['text'])

		if 'deletetask' in profiledata.keys():
			deletetask = await self.delete_task_profile(profiledata['deletetask'])
			usertaskprofiles = await self.user_task_profile()
			await self.send({
					"type":"websocket.send",
					"text": json.dumps({'usertaskprofiles':usertaskprofiles,'response':"Task Profile Deleted Successfully",})
			})

		if 'taskprofile' in profiledata.keys():
			profiledata = {data['name']:data['value'] for data in profiledata['taskprofile']}
			if 'taskid' in profiledata.keys():
				if len(profiledata['taskid']) != 0:
					try:
						taskprofile = await self.update_task_profile(profiledata)
						response = 'Profile Updated Successfully'
					except Exception as e:
						response = f"Error while updating taskprofile:{str(e)}"

				else:
					try:
						taskprofile = await self.save_task_profile(profiledata)
						response = 'Profile Saved Successfully'
					except Exception as e:
						response = f"Error while adding taskprofile:{str(e)}"
					
			usertaskprofiles = await self.user_task_profile()

			await self.send({
					"type":"websocket.send",
					"text": json.dumps({'usertaskprofiles':usertaskprofiles,'response':response,})
			})

		if 'profile' in profiledata.keys():
			show_profile = await self.show_task_profile(profiledata['profile'])
			await self.send({
					"type":"websocket.send",
					"text": json.dumps({'show_profile':show_profile})
			})

	@database_sync_to_async
	def save_task_profile(self, profiledata):
		profile_count = CreateTaskProfile.objects.filter(user=self.scope['user']).count()
		if profile_count >= 9 :
			CreateTaskProfile.objects.filter(user=self.scope['user'])[8].delete()
			profile_count = profile_count - 1
		CreateTaskProfile.objects.create(user=self.scope['user'],title=f"{str(self.scope['user']).title()}_Task_Profile_{profile_count}",select_action=profiledata['select_action'],	
		process_inbox=profiledata['process_inbox'],process_spam=profiledata['process_spam'],compose_mail=profiledata['compose_mail'],\
		archive_or_delete=profiledata['archive_or_delete'],bulk_notspam=profiledata['bulk_notspam'],add_safe_sender=profiledata['add_safe_sender'],\
		color_category=profiledata['color_category'],mark_flag=profiledata['mark_flag'],click_link=profiledata['click_link'],forward_mail=profiledata['forward_mail'],
		report_notspam=profiledata['report_notspam'],inbox_process_count=profiledata['inbox_process_count'],notspam_count=profiledata['notspam_count'],
		delete_count=profiledata['delete_count'],flag_count=profiledata['flag_count'],forward_count=profiledata['forward_count'],
		cc_count=profiledata['cc_count'],ss_count=profiledata['ss_count'],contact_count=profiledata['contact_count'],subject=profiledata['subject'],
		from_name=profiledata['from_name'])

		return True


	@database_sync_to_async
	def delete_task_profile(self, taskid):
		delete_task = CreateTaskProfile.objects.filter(id=taskid)
		delete_task.delete()
		return True


	@database_sync_to_async
	def update_task_profile(self, profiledata):
		profile_update = CreateTaskProfile.objects.get(id=profiledata['taskid'])
		profile_update.title = profiledata['title']
		profile_update.select_action = profiledata['select_action']
		profile_update.process_inbox = profiledata['process_inbox']
		profile_update.process_spam = profiledata['process_spam']
		profile_update.compose_mail = profiledata['compose_mail']
		profile_update.archive_or_delete = profiledata['archive_or_delete']
		profile_update.bulk_notspam = profiledata['bulk_notspam']
		profile_update.add_safe_sender = profiledata['add_safe_sender']
		profile_update.color_category = profiledata['color_category']
		profile_update.mark_flag = profiledata['mark_flag']
		profile_update.click_link = profiledata['click_link']
		profile_update.forward_mail = profiledata['forward_mail']
		profile_update.report_notspam = profiledata['report_notspam']
		profile_update.inbox_process_count = profiledata['inbox_process_count']
		profile_update.notspam_count = profiledata['notspam_count']
		profile_update.delete_count = profiledata['delete_count']
		profile_update.flag_count = profiledata['flag_count']
		profile_update.forward_count = profiledata['forward_count']
		profile_update.cc_count = profiledata['cc_count']
		profile_update.ss_count = profiledata['ss_count']
		profile_update.contact_count = profiledata['contact_count']
		profile_update.subject = profiledata['subject']
		profile_update.from_name = profiledata['from_name']
		profile_update.save()
		
		return True

	@database_sync_to_async
	def user_task_profile(self):
		usertaskprofiles = CreateTaskProfile.objects.filter(user=self.scope['user'])
		usertaskprofiles = [(i.id, i.title) for i in usertaskprofiles]
		return usertaskprofiles

	@database_sync_to_async
	def show_task_profile(self,title):
		try:
			usertaskprofiles = CreateTaskProfile.objects.get(title=title).__dict__
			del usertaskprofiles['_state']
		except:
			usertaskprofiles = ''
			pass
		return usertaskprofiles


	async def websocket_disconnect(self, event):
		print('------------CreateTaskProfileConsumer---------',event)



def insert_seed(user,team,tasklog,taskprofile,seed):
	# print('-------------in insert_seed----------',seed)
	flag = False
	try:
		UserSeed.objects.create(user=user, team =team,
			taskprofile=taskprofile,username=seed[0],password=seed[1],
			proxy='NA' if len(seed[2])==0 else seed[2],port='NA' if len(seed[3])==0 else seed[3],
			proxyuser='NA' if len(seed[4])==0 else seed[4],proxypass='NA' if len(seed[5])==0 else seed[5],
			recoverymail='NA' if len(seed[6])==0 else seed[6],emailto='NA' if len(seed[7])==0 else seed[7],
			forwardto='NA' if len(seed[8])==0 else seed[8],tasklog=tasklog)
		flag = True
	except Exception as e:
		if 'UNIQUE constraint failed' in str(e):
			print(e)

	return flag


import timeit
import itertools
class InsertTaskConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept"
		})

	async def websocket_receive(self, event):
		insertdata = json.loads(event['text'])
		inserttask = {data['name']:data['value'] for data in insertdata['inserttask']}
		# print('-------inserttask---------',inserttask)
		seedslists = [seed.strip('\r').split('\t') for seed in inserttask['seed'].split('\n')]
		seedslist = list(seed for seed,_ in itertools.groupby(seedslists))
		print('-------seedlist---------',seedslist)
		seedcounts = 0
		duplicates = len(seedslists)-len(seedslist)
		tasklog = f"{str(self.scope['user']).title()}_Task_{str(datetime.datetime.now())[:19].replace(' ','_')}"
		executor = ThreadPoolExecutor(1)
		user=self.scope['user']
		team =self.scope['session']['team']
		taskprofile = inserttask['selected_profile']
		start = timeit.default_timer()
		for seed in seedslist:
			if len(seed) == 9:
				# print('----------seed---------',seed)
			    future = executor.submit(insert_seed,user,team,tasklog,taskprofile,seed)
			    seedcounts+=1
			    response = f"{seedcounts} seeds inserted successfully, {duplicates} duplicate seeds found."
			else:
				response = "data not in given format, please insert data in proper format."
		stop = timeit.default_timer()
		print('Time: ', stop - start)  
		user_unique_seed_task = await self.get_user_unique_seed_task()
		await self.send({
					"type":"websocket.send",
					"text": json.dumps({'response':response,'user_unique_seed_task':user_unique_seed_task})
			})
				
	async def websocket_disconnect(self, event):
		pass

	@database_sync_to_async
	def get_user_unique_seed_task(self):
		user_unique_seed_task = list(UserSeed.objects.filter(tasklog__icontains=self.scope['user']).values_list('tasklog',flat=True).distinct())
		uniquetask = []
		for i,j in enumerate(user_unique_seed_task):
			uniquetask.append({'id':i+1,'tasklog':j})
		return uniquetask




class RemoveSeedsConsumer(AsyncConsumer):
	async def websocket_connect(self,event):
		await self.send({
			"type":"websocket.accept"
		})

		user_unique_seed_task = await self.get_user_unique_seed_task()
		alluniquetask = await self.get_all_unique_seed_task()
		await self.send({
				"type":"websocket.send",
				"text": json.dumps({'user_unique_seed_task':user_unique_seed_task,'alluniquetask':alluniquetask})
		})

	async def websocket_receive(self,event):
		seedtask = json.loads(event['text'])
		print('---------seedtask---------',seedtask)
		json_response = {}
		if 'seeduniquetask' in seedtask.keys():
			task_wise_seed, labels, data = await self.get_unique_task_wise_seed(seedtask['seeduniquetask'])
			json_response['task_wise_seed'] = task_wise_seed
			json_response['labels'] = labels
			json_response['data'] = data
		
		if 'deleteuniquetask' in seedtask.keys():
			response = await self.delete_task_all_seed(seedtask['deleteuniquetask'])
			json_response['response'] = response
			json_response['user_unique_seed_task'] = await self.get_user_unique_seed_task()
			json_response['alluniquetask'] = await self.get_all_unique_seed_task()
			json_response['task_wise_seed'] = []

		if 'deleteuniquetaskseed' in seedtask.keys():
			seeduniquetask = UserSeed.objects.get(id=seedtask['deleteuniquetaskseed'])
			taskname = seeduniquetask.tasklog
			seeduniquetask.delete()
			task_wise_seed, labels, data = await self.get_unique_task_wise_seed(taskname)
			json_response['user_unique_seed_task'] = await self.get_user_unique_seed_task()
			json_response['task_wise_seed'] = task_wise_seed
			json_response['response'] = 'Seed Record Deleted Successfully'

		await self.send({
				"type":"websocket.send",
				"text": json.dumps(json_response)
		})

	async def websocket_disconnect(self,event):
		pass


	@database_sync_to_async
	def get_user_unique_seed_task(self):
		user_unique_seed_task = list(UserSeed.objects.filter(tasklog__icontains=self.scope['user']).values_list('tasklog',flat=True).distinct())
		uniquetask = []
		for i,j in enumerate(user_unique_seed_task):
			uniquetask.append({'id':i+1,'tasklog':j})
		return uniquetask

	@database_sync_to_async
	def get_all_unique_seed_task(self):
		user_unique_seed_task = list(UserSeed.objects.order_by().values('tasklog').distinct())
		alluniquetask = []
		for i,j in enumerate(user_unique_seed_task):
			alluniquetask.append({'id':i+1,'tasklog':j.get('tasklog')})
		return alluniquetask

	@database_sync_to_async
	def get_unique_task_wise_seed(self, taskname):
		task_wise_seed = UserSeed.objects.filter(tasklog=taskname)
		labels = list(UserSeed.objects.filter(tasklog=taskname).values_list('seedstatus',flat=True).distinct())
		data = [UserSeed.objects.filter(tasklog=taskname,seedstatus=label).count() for label in labels]
		task_wise_seed = [{"id":i.id,"username":i.username,"password":i.password,"proxy":i.proxy,"port":i.port,"recoverymail":i.recoverymail,"emailto":i.emailto,"forwardto":i.forwardto,"taskprofile":i.taskprofile,"seedstatus":i.seedstatus} for i in task_wise_seed]
		return task_wise_seed, labels, data

	@database_sync_to_async
	def delete_task_all_seed(self,taskname):
		try:
			UserSeed.objects.filter(tasklog=taskname).delete()
			response = 'Task Deleted Successfully'
		except Exception as e:
			response = str(e)
		return response
