from django.contrib.auth.models import User
from django.db import models

from .utils import *


# Create your models here.
class EventRecord(models.Model):
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=50)
    c_o_e = models.CharField(max_length=75)
    event_name = models.CharField(max_length=110)
    description = models.TextField(max_length=2010)
    duration_number = models.CharField(max_length=10)
    duration_string = models.CharField(max_length=10)
    resource_person = models.CharField(max_length=110)
    resource_person_data = models.TextField(max_length=2010)
    registration_start = models.DateField()
    registration_end = models.DateField()
    event_date = models.DateField()
    eligible_branches = models.CharField(max_length=50)
    outside_student = models.IntegerField(default=0)
    venue = models.TextField(max_length=2010)
    registered_student = models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
