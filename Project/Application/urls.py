from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
	path('', Login, name = 'Login'),
	path('logout', Logout, name = 'Logout'),
	path('homepage', Homepage, name = 'Homepage'),
]