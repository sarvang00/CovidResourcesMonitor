from django.db import models
from datetime import datetime
from teams.models import Location, Resource, LeadType

class ProposedLead(models.Model):
    lead_name = models.CharField(max_length=100)
    contact_num = models.CharField(max_length=100)
    proposed_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='proposed_location')
    full_address = models.TextField(blank=True, null=True)
    gmaps_url = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    lead_type = models.ForeignKey(LeadType, on_delete=models.DO_NOTHING, related_name='proposed_leadtype')
    source = models.BooleanField()
    comments = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(default=datetime.now)

class ProposedAvailability(models.Model):
    lead = models.ForeignKey(ProposedLead, on_delete=models.CASCADE, related_name='lead')
    proposed_resource_type = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, related_name='proposed_resource_type')
    available_count = models.IntegerField(default=0)
    