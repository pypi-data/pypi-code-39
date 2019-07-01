from datetime import datetime
from pytz import timezone
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin import DateFieldListFilter
from .models import Candidate, Category, Faq, Issue, Position, Story, Update


class UpdateAdmin(admin.ModelAdmin):
    readonly_fields = ["text", "issue", "category", "created_on"]
    list_display = ("page", "time", "day")
    list_filter = (("created_on", DateFieldListFilter),)

    def time(self, obj):
        eastern = timezone("US/Eastern")
        return obj.created_on.astimezone(eastern).strftime("%I:%M %p")

    def day(self, obj):
        eastern = timezone("US/Eastern")
        return obj.created_on.astimezone(eastern).strftime("%B %d, %Y")

    def page(self, obj):
        if obj.issue:
            url = reverse(
                "issuestracker:issue", kwargs={"issue": obj.issue.slug}
            )
        elif obj.category:
            url = reverse(
                "issuestracker:category",
                kwargs={"category": obj.category.slug},
            )
        else:
            return obj.page()

        return format_html('<a href="{}">{}</a>', url, obj.page())

    page.allow_tags = True
    page.short_description = "Page"

    def __init__(self, *args, **kwargs):
        super(UpdateAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None


admin.site.register(Candidate)
admin.site.register(Category)
admin.site.register(Faq)
admin.site.register(Issue)
admin.site.register(Position)
admin.site.register(Story)
admin.site.register(Update, UpdateAdmin)
