from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.utils.safestring import mark_safe
# from . login_db import login_instance
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.models import User
from . models import MachineConfiguration, CreateTaskProfile
from django.http import Http404

# from Project.tasks import add



def Login(request):	
	context = {}
	# for i in range(1000):
	# 	print('-------------tasks-------------',add.delay(100,i))
	try:
		if request.method == 'POST':
			userEmail = request.POST.get('username')
			userPasswd = request.POST.get('password')
			print('-----username------password-----',userEmail,userPasswd)
			if userEmail == 'root' and userPasswd == 'pass1234':
				# userEmail = 'balasahebg@fecdirect.net'
				# userPasswd = 'k7s41ga'
				# result = login_instance.matchUserPass(userEmail,userPasswd)
				userTeam, userRole, userEmpId = 'A' , 'Programmer', '5490'
				request.session['username'] = userEmail
				request.session['password'] = userPasswd
				request.session['team'] = userTeam
				request.session['role'] = userRole
				request.session['empid'] = userEmpId
				try:
					user = authenticate(username=userEmail, password=userPasswd)
					login(request, user)
				except:
					new_user = User(username=userEmail, password=userPasswd)
					new_user.set_password(userPasswd)
					new_user.save()
					login(request, new_user)

				return redirect('Homepage')


			if userEmail == 'balasaheb' and userPasswd == 'Gulave@123':
				# userEmail = 'balasahebg@fecdirect.net'
				# userPasswd = 'k7s41ga'
				# result = login_instance.matchUserPass(userEmail,userPasswd)
				userTeam, userRole, userEmpId = 'A' , 'Programmer', '5490'
				request.session['username'] = userEmail
				request.session['password'] = userPasswd
				request.session['team'] = userTeam
				request.session['role'] = userRole
				request.session['empid'] = userEmpId
				try:
					user = authenticate(username=userEmail, password=userPasswd)
					login(request, user)
				except:
					new_user = User(username=userEmail, password=userPasswd)
					new_user.set_password(userPasswd)
					new_user.save()
					login(request, new_user)

				return redirect('Homepage')

			else:
				context['login_error'] = 'Invalid email and password'
	except Exception as e:
		print('--------Login-Error--------',e)
		raise Http404

	return render(request, 'Application/login.html', context)

@login_required(login_url='Login')
def Homepage(request):
	context = {}
	try:
		default_profile = CreateTaskProfile.objects.filter(title=f"{str(request.user).title()}_Default_Profile").count()
		print('---------count---------',default_profile)
		if default_profile == 0:
			CreateTaskProfile.objects.create(user=request.user,title=f"{str(request.user).title()}_Default_Profile")
	except Exception as e:
		print('---------default_profile err---------',e)
		pass

	try:
		user_team_machines = MachineConfiguration.objects.filter(team = request.session['team'])
		context['user_team_machines'] = user_team_machines
		check_admin = request.user.is_superuser
		if check_admin == True:
			context['check_admin'] = check_admin
		context['team'] = request.session['team']
		context['role'] = request.session['role']
		context['empid'] = request.session['empid']
	except Exception as e:
		print('--------Homepage-Error--------',e)
		raise Http404
	print('------------',request.user,request.session.keys())
	return render(request, 'Application/index.html', context)

@login_required(login_url='Login')
def Logout(request):
	try:
		logout(request)
	except Exception as e:
		print('--------Logout-Error--------',e)
		raise Http404
	return redirect('Login')

def Deletemachine(request,pk=None):
	try:
		instance = MachineConfiguration.objects.get(id=pk)
		instance.delete()
	except Exception as e:
		print('-----------Deletemachine-Error-----------',e)
	return redirect('Homepage')
	 
