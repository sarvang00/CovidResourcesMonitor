from django.db import models
from django.conf import settings
from datetime import datetime

class Location(models.Model):
    state = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

class LeadType(models.Model):
    type = models.CharField(max_length=100)

class Resource(models.Model):
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)

class Lead(models.Model):
    lead_name = models.CharField(max_length=100)
    contact_num = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location')
    full_address = models.TextField(blank=True, null=True)
    gmaps_url = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    lead_type = models.ForeignKey(LeadType, on_delete=models.DO_NOTHING, related_name='leadtype')
    source = models.BooleanField() #true for self added, false for lead by others
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(default=datetime.now)

class Availability(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead')
    resource_type = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, related_name='resource_type')
    available_count = models.IntegerField(default=0)
    