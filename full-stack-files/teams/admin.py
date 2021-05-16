from django.contrib import admin

from .models import Location, Resources, Lead, Availability

admin.site.register(Location)
admin.site.register(Resources)
admin.site.register(Lead)
admin.site.register(Availability)