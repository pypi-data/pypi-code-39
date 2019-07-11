from django.db import models
from django.db.models import Q, Count


class LiveManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status="live")
            .exclude(last_published=None)
        )


class LiveCandidateManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                position_count=Count(
                    "position", filter=Q(position__issue__status="live")
                )
            )
            .filter(Q(position_count__gt=0))
        )
