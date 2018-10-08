from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class WorkshopRecord(models.Model):
    slug = models.CharField(unique=True, max_length=55)
    event_name = models.CharField(max_length=55)
    description = models.TextField(max_length=1010)
    duration = models.CharField(max_length=25)
    resource_person = models.CharField(max_length=55)
    resource_person_data = models.TextField(max_length=510)
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    event_date = models.IntegerField()
    event_month = models.CharField(max_length=25)
    event_year = models.IntegerField()
    eligible_branches = models.CharField(max_length=10)
    outside_student = models.CharField(max_length=5)
    venue = models.TextField(max_length=1010)
    registered= models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.slug