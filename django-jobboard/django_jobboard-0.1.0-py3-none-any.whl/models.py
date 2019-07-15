import uuid

from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# STATUS_CATEGORIES = getattr(settings, "JOBBOARD_STATUS_CATEGORIES", [(1, "Queued"), (2, "Active"), (3, "Paused"), (4, "Complete")])
JOB_LEVEL_CATEGORIES = getattr(settings, "JOBBOARD_JOB_LEVEL_CATEGORIES", [(1, "Junior"), (2, "Mid"), (3, "Senior"), (4, "Lead"), (5, "Specialist")])
ASSESSED_LEVEL = getattr(settings, "JOBBOARD_ASSESSED_LEVEL", [(1, "Under Qualified"), (2, "Below Expectations"), (3, "Meets Expectation"), (4, "Exceeds Expectations"), (5, "Over Qualified")])
# APPLICANT_EVENT_TYPES = [(1, "General"), (2, "New Entry"), (3, "Submission Review"), (4, "Pass - Screening")]
EMPLOYMENT_CHOICES = getattr(settings, "JOBBOARD_EMPLOYMENT_CHOICES", [('full-time',"Full Time"),('part-time',"Part Time"),('contract',"Contract"),])


class Department(models.Model):
    '''
    What department is this for?
    '''
    name = models.CharField(_("Name"), max_length=40, blank=False)
    slug = models.SlugField(_("Slug"), blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify( self.name )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    '''
    What where is this job located
    '''
    name = models.CharField(_("Name"), max_length=40, blank=False)
    slug = models.SlugField(_("Slug"), blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify( self.name )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    title = models.CharField(_("Title"), max_length=40, blank=False)
    slug = models.SlugField(_("Slug"), blank=True)
    active = models.BooleanField(_("Active"), default=True)
    level = models.IntegerField(_("Level"), choices=JOB_LEVEL_CATEGORIES)

    sites = models.ManyToManyField(Site)

    department = models.ForeignKey('Department', on_delete=models.CASCADE, blank=False)
    employment = models.CharField(max_length=20, blank=False, choices=EMPLOYMENT_CHOICES)   # Full-Time/PT
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=False)

    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    plusses = models.TextField(blank=True)

    salary_high = models.IntegerField(blank=True, null=True)
    salary_low = models.IntegerField(blank=True, null=True)

    created = models.DateTimeField("Date Created", auto_now_add=True)
    updated = models.DateTimeField("Last Updated", auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify( self.department.name + " " + self.title + " " + self.location.name )
        super(JobPosting, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Job Posting")
        verbose_name_plural = _("Job Postings")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("jobposting_detail", kwargs={"slug": self.slug})


# class ApplicationStatus(models.Model):
#     '''
#     The Status levels of the Application, such as "New", "Processing" and "Hired".
#     '''
#     name = models.CharField(_("Name"), max_length=40, blank=False)
#     category = models.IntegerField(_("Category"), choices=STATUS_CATEGORIES)


# class ApplicationEventType(models.Model):
#     '''
#     The Event Type of the Application, "New Entry".
#     '''
#     name = models.CharField(_("Name"), max_length=40, blank=False)
#     category = models.IntegerField(_("Category"), choices=STATUS_CATEGORIES)


# class Applicant(models.Model):
#     first_name = models.CharField(_("Title"), max_length=40, blank=False)
#     last_name = models.CharField(_("Title"), max_length=40, blank=False)
#     posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
#     cover_letter = models.TextField()
#     email = models.EmailField()
#     status = models.ForeignKey('ApplicationStatus', on_delete=models.CASCADE)
#     atrophy = models.DateTimeField()  # When was the last thing something happened with this Applicant?


# class Feedback(models.Model):
#     applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
#     level = models.IntegerField(_("Level"), choices=ASSESSED_LEVEL)
#     skills = models.TextField()
#     personality = models.TextField()
#     work_ethic = models.TextField()
#     interviewer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# class Event(models.Model):
#     applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
#     etype = models.ForeignKey('ApplicationEventType', on_delete=models.CASCADE)
#     logline = models.TextField()
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
