from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'guests/guest-dashboard.html')

def contribute(request):
    return render(request, 'guests/guest-contribute.html')

def login(request):
    return render(request, 'guests/login.html')