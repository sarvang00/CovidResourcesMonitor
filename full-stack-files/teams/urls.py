from django.urls import path

from . import views

urlpatterns = [
    path('teamdashboard', views.teamDashboard, name='teamdashboard'),
    path('addleads', views.addLeads, name='addleads'),
    path('admincontrols', views.adminControls, name='admincontrols'),
]