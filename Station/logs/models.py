from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
import time


class Event(models.Model):
    LocationTypes = (('Unknown', 'Unknown'),('Lube', 'Lube'),('Vacuum', 'Vacuum'),('Washing', 'Washing'))
    LocationType = models.CharField(max_length=200,choices=LocationTypes,default=0)

    Camera = models.CharField(max_length=200, blank=True, null=True)
    Location = models.CharField(max_length=200, blank=True, null=True)

    PlatesNo = models.CharField(max_length=200, blank=True, null=True)
    PlatesRegion = models.CharField(max_length=200, blank=True, null=True)
    PlatesScore = models.CharField(max_length=200, blank=True, null=True)

    VehicleType = models.CharField(max_length=200, blank=True, null=True)

    EntryTime = models.DateTimeField(null=True, blank=True)
    ExitTime = models.DateTimeField(null=True, blank=True)

    VehicleImage = models.FileField(upload_to='Events/%Y/%m/%d/', blank=True)
    PlateImage = models.FileField(upload_to='Events/%Y/%m/%d/', blank=True)

    LPRResult = models.CharField(max_length=4096, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
	    return str(self.LocationType) + " "+ str(self.PlatesNo)

    def save(self, *args, **kwargs):
	    super(Event, self).save(*args, **kwargs)