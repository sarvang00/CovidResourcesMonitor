from django.contrib import admin

from .models import ProposedLead, ProposedAvailability

class ProposedLeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead_name', 'contact_num', 'proposed_location', 'email', 'lead_type')
    list_display_links = ('id', 'lead_name')
    list_filter = ('proposed_location', 'lead_type')
    search_fields = ('proposed_location', 'lead_type')
    list_per_page = 25

class ProposedAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'proposed_resource_type', 'available_count')
    list_display_links = ('id', 'lead')
    list_filter = ('proposed_resource_type',)
    search_fields = ('lead', 'proposed_resource_type')
    list_per_page = 25

admin.site.register(ProposedLead, ProposedLeadAdmin)
admin.site.register(ProposedAvailability, ProposedAvailabilityAdmin)