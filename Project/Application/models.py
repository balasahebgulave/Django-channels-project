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
	cpu_usage = models.CharField(max_length=10, default='Not Active')
	ram_usage = models.CharField(max_length=10, default='Not Active')

	# def __str__(self):
	# 	return f"Team : {self.team} : {self.machine_ip}"


class CreateTaskProfile(models.Model):
	user = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	select_action = models.CharField(max_length=100, default='Default')
	process_inbox = models.CharField(max_length=100, default='Yes')
	process_spam = models.CharField(max_length=100, default='Yes')
	compose_mail = models.CharField(max_length=100, default='No')
	archive_or_delete = models.CharField(max_length=100, default='None')
	bulk_notspam = models.CharField(max_length=100, default='No')
	add_safe_sender = models.CharField(max_length=100, default='No')
	color_category = models.CharField(max_length=100, default='No')
	mark_flag = models.CharField(max_length=100, default='No')
	click_link = models.CharField(max_length=100, default='Yes')
	forward_mail = models.CharField(max_length=100, default='No')
	report_notspam = models.CharField(max_length=100, default='No')
	inbox_process_count = models.CharField(max_length=100, default='0')
	notspam_count = models.CharField(max_length=100, default='0')
	delete_count = models.CharField(max_length=100, default='0')
	flag_count = models.CharField(max_length=100, default='0')
	forward_count = models.CharField(max_length=100, default='0')
	cc_count = models.CharField(max_length=100, default='0')
	ss_count = models.CharField(max_length=100, default='0')
	contact_count = models.CharField(max_length=100, default='0')
	subject = models.CharField(max_length=100, default='None')
	from_name = models.CharField(max_length=100, default='None')

	# def __str__(self):
	# 	return f"Team : {self.title}"


