from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.utils.safestring import mark_safe
from . login_db import login_instance
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.models import User


def Login(request):	
	context = {}
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

	return render(request, 'Application/login.html', context)

# @login_required(login_url='Login')
def Homepage(request):
	context = {}
	check_admin = request.user.is_superuser
	if check_admin == True:
		context['check_admin'] = check_admin
	context['team'] = request.session['team']
	context['role'] = request.session['role']
	context['empid'] = request.session['empid']
	print('------------',request.user,request.session.keys())
	return render(request, 'Application/index.html', context)

@login_required(login_url='Login')
def Logout(request):
	# keys = ['username','password','team','role','empid']
	# for i in keys:
	# 	del request.session[i]
	logout(request)
	return redirect('Login')
