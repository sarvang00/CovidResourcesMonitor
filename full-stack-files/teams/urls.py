from django.urls import path

from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('addleads', views.addLeads, name='addleads'),
    path('admincontrols', views.adminControls, name='admincontrols'),
]