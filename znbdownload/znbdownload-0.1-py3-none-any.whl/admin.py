from django.contrib import admin

from .models import Download, PrivateDownload


class DownloadAdmin(admin.ModelAdmin):
    pass


class PrivateDownloadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Download, DownloadAdmin)
admin.site.register(PrivateDownload, PrivateDownloadAdmin)
