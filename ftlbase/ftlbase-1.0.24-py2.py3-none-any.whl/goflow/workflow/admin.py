from django.contrib import admin

from .models import *


class TransitionInline(admin.StackedInline):
    model = Transition
    fieldsets = ((None, {'fields': ('description', ('input', 'output'), 'condition', 'precondition')}),)


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'summary', 'priority')
    inlines = [
        TransitionInline,
    ]


admin.site.register(Process, ProcessAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('url', 'documentation', 'test')


admin.site.register(Application, ApplicationAdmin)


class PushApplicationAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('url', 'documentation', 'test')


admin.site.register(PushApplication, PushApplicationAdmin)


class ActivityAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('title', 'description', 'kind', 'application',
                    'join_mode', 'split_mode', 'autostart', 'autofinish', 'process')
    list_filter = ('process', 'kind')
    fieldsets = (
        (None, {'fields': (('kind', 'subflow'), ('title', 'process'), 'description')}),
        ('Push application', {'fields': (('push_application', 'pushapp_param'),)}),
        ('Application', {'fields': (('application', 'app_param'),)}),
        ('I/O modes', {'fields': (('join_mode', 'split_mode'),)}),
        ('Execution modes', {'fields': (('autostart', 'autofinish', 'sendmail', 'approve', 'ratify'),)}),
        ('Permission', {'fields': ('roles',)}),
    )


admin.site.register(Activity, ActivityAdmin)


class TransitionAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('__str__', 'process', 'input', 'output', 'condition', 'description')
    list_filter = ('process',)
    fieldsets = (
        (None, {'fields': (('name', 'description'), 'process', ('input', 'output'), 'condition', 'precondition')}),
    )


admin.site.register(Transition, TransitionAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'web_host', 'notified', 'last_notif', 'nb_wi_notif', 'notif_delay')
    list_filter = ('web_host', 'notified')


admin.site.register(UserProfile, UserProfileAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
