from django.shortcuts import render, redirect
from django.contrib import messages, auth


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admincontrols')
        else:
            return redirect('teamdashboard')
    else:
        return redirect('dashboard')

def dashboard(request):
    return render(request, 'guests/guest-dashboard.html')

def contribute(request):
    return render(request, 'guests/guest-contribute.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'guests/login.html')

