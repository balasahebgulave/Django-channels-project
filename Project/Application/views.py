from django.shortcuts import render
from django.http import HttpResponse
import json
from django.utils.safestring import mark_safe

def Homepage(request):
	return render(request, 'Application/index.html')

