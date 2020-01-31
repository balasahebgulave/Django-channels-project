from django.db import models

class UserSeed(models.Model):
	user = models.CharField(max_length = 100, blank=False)
	team = models.CharField(max_length = 100, blank=False)
	taskprofile = models.CharField(max_length = 100, default='None')
	username = models.CharField(max_length = 100, default='None')
	password = models.CharField(max_length = 100, default='None')
	proxy = models.CharField(max_length = 100, default='None')
	port = models.CharField(max_length = 100, default='None')
	proxyuser = models.CharField(max_length = 100, default='None')
	proxypass = models.CharField(max_length = 100, default='None')
	recoverymail = models.CharField(max_length = 100, default='None')
	emailto = models.CharField(max_length = 100, default='None')
	forwardto = models.CharField(max_length = 100, default='None')
	tasklog = models.CharField(max_length = 100, default='None')
	seedlog = models.CharField(max_length = 100, default='None')
	
	# def __str__(self):
	# 	return self.user


class MachineConfiguration(models.Model):
	team = models.CharField(max_length=20, blank = False)
	machine_ip = models.CharField(max_length=50, blank = False)
	adminuser = models.CharField(max_length=100, blank = False)
	password = models.CharField(max_length=100, blank = False)
	cpu_usage = models.CharField(max_length=10, default='Not Active')
	ram_usage = models.CharField(max_length=10, default='Not Active')
	disk_usage = models.CharField(max_length=10, default='Not Active')

	# def __str__(self):
	# 	return f"Team : {self.team} : {self.machine_ip}"


class CreateTaskProfile(models.Model):
	user = models.CharField(max_length=100, blank = False)
	title = models.CharField(max_length=100, blank = False)
	select_action = models.CharField(max_length=100, default='S_A_Default')
	process_inbox = models.CharField(max_length=100, default='P_I_Yes')
	process_spam = models.CharField(max_length=100, default='P_S_Yes')
	compose_mail = models.CharField(max_length=100, default='C_M_No')
	archive_or_delete = models.CharField(max_length=100, default='None')
	bulk_notspam = models.CharField(max_length=100, default='B_N_S_No')
	add_safe_sender = models.CharField(max_length=100, default='A_S_No')
	color_category = models.CharField(max_length=100, default='C_C_No')
	mark_flag = models.CharField(max_length=100, default='M_F_No')
	click_link = models.CharField(max_length=100, default='C_L_Yes')
	forward_mail = models.CharField(max_length=100, default='F_M_No')
	report_notspam = models.CharField(max_length=100, default='R_N_S_No')
	inbox_process_count = models.CharField(max_length=100, default='25')
	notspam_count = models.CharField(max_length=100, default='25')
	delete_count = models.CharField(max_length=100, default='0')
	flag_count = models.CharField(max_length=100, default='0')
	forward_count = models.CharField(max_length=100, default='0')
	cc_count = models.CharField(max_length=100, default='0')
	ss_count = models.CharField(max_length=100, default='0')
	contact_count = models.CharField(max_length=100, default='0')
	subject = models.CharField(max_length=100, default='NA')
	from_name = models.CharField(max_length=100, default='NA')

	# def __str__(self):
	# 	return f"Team : {self.title}"






