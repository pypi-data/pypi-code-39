from django.contrib import admin

from jobboard.models import JobPosting, Department, Location

class JobPostingAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('title', 'department', 'active')

class DepartmentAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

class LocationAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Location, LocationAdmin)