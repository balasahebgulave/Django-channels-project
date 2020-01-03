from django.db import models

class UserSeed(models.Model):
	proxy = models.CharField(max_length = 100, default='None')
	username = models.CharField(max_length = 100, default='None')
	password = models.CharField(max_length = 100, default='None')
	recoverymail = models.CharField(max_length = 100, default='None')
	user = models.CharField(max_length = 100)

	# def __str__(self):
	# 	return self.user


class MachineConfiguration(models.Model):
	team = models.CharField(max_length=20, blank = False)
	machine_ip = models.CharField(max_length=50, blank = False)
	adminuser = models.CharField(max_length=100, blank = False)
	password = models.CharField(max_length=100, blank = False)

	# def __str__(self):
	# 	return f"Team : {self.team} : {self.machine_ip}"

