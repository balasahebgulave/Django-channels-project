from django.db import models

class Userseeds(models.Model):
	proxy = models.CharField(max_length = 100, default='None')
	username = models.CharField(max_length = 100, default='None')
	password = models.CharField(max_length = 100, default='None')
	recoverymail = models.CharField(max_length = 100, default='None')
	user = models.CharField(max_length = 100)

	def __str__(self):
		return self.user


