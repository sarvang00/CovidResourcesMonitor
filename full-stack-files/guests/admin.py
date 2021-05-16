from django.contrib import admin

from .models import ProposedLead, ProposedAvailability

admin.site.register(ProposedLead)
admin.site.register(ProposedAvailability)