from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Process(models.Model):
    """
    Record process from Activity Service.
    """
    process_key = models.CharField(
        _('Process Key'), max_length=128, unique=True, db_index=True)
    process_type_slug = models.CharField(
        _('Process Type'), max_length=128)
    internal_key = models.CharField(
        _('Internal Key'), max_length=128)
    status = models.CharField(_('Status'), max_length=128)


class Activity(models.Model):
    """
    Record activity from Activity Service.
    """
    activity_id = models.PositiveIntegerField(unique=True, db_index=True)
    process = models.ForeignKey(
        Process,
        verbose_name=_('Process'),
        related_name='activities',
        on_delete=models.CASCADE,
    )
    from_template_activity_slug = models.CharField(
        _('Template Activity Slug'), max_length=128)
