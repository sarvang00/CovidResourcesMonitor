from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('contribute', views.contribute, name='contribute'),
    path('login', views.login, name='login'),
]