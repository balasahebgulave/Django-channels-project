from celery import shared_task

@shared_task
def add(a=10,b=20):
	return a+b