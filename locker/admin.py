import csv

from django.contrib import admin
from .models import User, Device
from django.http import HttpResponse

class ExportCsv:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar selecionados em CSV"


class UserAdmin(admin.ModelAdmin, ExportCsv):

    list_display = ('date_time', 'name', 'uid', 'enabled', 'autorized')
    list_filter = ['date_time']
    actions = ["export_as_csv"]
    search_fields = ['uid']
    list_per_page = 50
    

class DeviceAdmin(admin.ModelAdmin, ExportCsv):

    list_display = ('date_time', 'device_id', 'door_status', 'uid')
    list_filter = ['date_time', 'device_id', 'door_status']
    actions = ["export_as_csv"]

    list_per_page = 50

    #search_fields = ['device_id', 'typ']
    
admin.site.register(User, UserAdmin)
admin.site.register(Device, DeviceAdmin)

