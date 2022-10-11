from django.contrib import admin
from . import models
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
# Register your models here.

class EventAdmin(ImportExportModelAdmin):
    list_display = ('LocationType','Camera','Location','PlatesRegion','PlatesNo','VehicleType','EntryTime','ExitTime','created')
    list_filter = ('created',('created', DateRangeFilter),('EntryTime', DateRangeFilter),('ExitTime', DateRangeFilter),'VehicleType')
    search_fields = ['Location','PlatesNo']

admin.site.register(models.Event,EventAdmin)
