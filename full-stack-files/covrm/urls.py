from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('guests.urls')),
    path('admin/', admin.site.urls),
]
