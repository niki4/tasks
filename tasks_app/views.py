from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Use POST request to set new task")