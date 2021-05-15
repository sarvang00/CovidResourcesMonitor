from django.shortcuts import render

def teamDashboard(request):
    return render(request, 'teams/team-dashboard.html')

def addLeads(request):
    return render(request, 'teams/team-add-modify.html')

def adminControls(request):
    return render(request, 'teams/admin-dashboard.html')