import codecs
import csv
from django.contrib import admin
from django.shortcuts import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'language', 'country', 'uploaded', 'created')
    list_filter = ('language', 'country', 'uploaded')
    search_fields = ('first_name', 'last_name', 'email')
    actions = ('export_selected', )

    def export_selected(self, request, queryset):
        opts = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename={}.csv'.format(
            opts.verbose_name_plural.replace(' ', '_')
        )
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response, delimiter=';')

        fields = [
            _('id'), _('first name'), _('last name'), _('email'), _('language'), _('country'),  _('date/time')
        ]
        # Write a first row with header information
        writer.writerow(fields)
        # Write data rows
        for obj in queryset:
            data_row = list()
            data_row.append(obj.id)
            data_row.append(obj.first_name)
            data_row.append(obj.last_name)
            data_row.append(obj.email)
            data_row.append(obj.language)
            data_row.append(obj.country.code)
            data_row.append(obj.created.strftime('%d/%m/%Y %H:%M:%S'))
            writer.writerow(data_row)
        return response

    export_selected.short_description = _('Export selected subscribers')
