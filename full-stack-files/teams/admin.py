from django.contrib import admin

from .models import LeadType, Location, Resource, Lead, Availability

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead_name', 'contact_num', 'location', 'email', 'lead_type')
    list_display_links = ('id', 'lead_name')
    list_filter = ('location', 'lead_type')
    search_fields = ('location', 'lead_type')
    list_per_page = 25

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'resource_type', 'available_count')
    list_display_links = ('id', 'lead')
    list_filter = ('resource_type',)
    search_fields = ('lead', 'resource_type')
    list_per_page = 25

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'sub_category')
    list_filter = ('category',)
    search_fields = ('category', 'sub_category')
    list_per_page = 25

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'region')
    list_filter = ('state',)
    search_fields = ('state', 'region')
    list_per_page = 25

class LeadTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type', )
    list_per_page = 25

admin.site.register(Location, LocationAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(LeadType, LeadTypeAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Availability, AvailabilityAdmin)