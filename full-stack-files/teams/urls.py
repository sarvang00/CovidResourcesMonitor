from django.urls import path

from . import views

urlpatterns = [
    path('teamdashboard', views.teamDashboard, name='teamdashboard'),
    path('addleads', views.addLeads, name='addleads'),
    path('admincontrols', views.adminControls, name='admincontrols'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logout, name='logout'),
    path('addcategory', views.addCategory, name='addcategory'),
    path('addsubcategory', views.addSubCategory, name='addsubcategory'),
]