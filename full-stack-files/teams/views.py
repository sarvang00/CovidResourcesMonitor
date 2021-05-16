from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def teamDashboard(request):
    return render(request, 'teams/team-dashboard.html')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def addLeads(request):
    return render(request, 'teams/team-add-modify.html')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def adminControls(request):
    return render(request, 'teams/admin-dashboard.html')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def registerUser(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
                return redirect('admincontrols')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is laready in use!')
                    return redirect('admincontrols')
                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(
                        request, 'User is now registered and can log in')
                    return redirect('admincontrols')
        else:
            messages.error(request, 'Passwords donot match')
            return redirect('admincontrols')
    else:
        return redirect('admincontrols')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('dashboard')
