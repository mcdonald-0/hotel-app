from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request, *args, **kwargs):
	context = {}
	return HttpResponse('<h1>This is the index page</h1>')