from django.shortcuts import render, redirect

def index(request):
    return redirect('dashboard')

def dashboard(request):
    return render(request, 'guests/guest-dashboard.html')

def contribute(request):
    return render(request, 'guests/guest-contribute.html')

def login(request):
    return render(request, 'guests/login.html')