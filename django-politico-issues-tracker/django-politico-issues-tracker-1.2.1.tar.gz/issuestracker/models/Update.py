from django.db import models


class Update(models.Model):
    """
    An update about an issue (e.g. "Cory Booker now supports X.")
    """

    text = models.TextField(null=True, blank=True)
    issue = models.ForeignKey(
        "Issue",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="updates",
        related_query_name="updates",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="updates",
        related_query_name="updates",
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.created_on, self.text if self.text else "")

    def page(self):
        if self.category:
            return self.category
        if self.issue:
            return self.issue
        return None

    class Meta:
        ordering = ["-created_on"]
