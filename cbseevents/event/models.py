from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from .utils import get_unique_slug


# Create your models here.
class EventRecord(models.Model):
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=50)
    c_o_e = models.CharField(max_length=75)

    event_name = models.CharField(max_length=110)
    event_pic = models.FileField(default='')
    fees = models.FloatField()
    registration_start = models.DateField()
    registration_end = models.DateField()
    event_date = models.DateField()
    duration_number = models.CharField(max_length=10)
    duration_string = models.CharField(max_length=10)
    eligible_branches = models.CharField(max_length=75)

    pre_requisites_1 = models.CharField(max_length=50, default='')
    pre_requisites_2 = models.CharField(max_length=50, default='')
    pre_requisites_3 = models.CharField(max_length=50, default='')
    learning_outcome_1= models.CharField(max_length=50, default='')
    learning_outcome_2= models.CharField(max_length=50, default='')
    learning_outcome_3= models.CharField(max_length=50, default='')
    learning_outcome_4= models.CharField(max_length=50, default='')
    learning_outcome_5= models.CharField(max_length=50, default='')
    learning_outcome_6= models.CharField(max_length=50, default='')
    description = RichTextUploadingField()

    outside_student = models.IntegerField(default=0)
    venue = models.CharField(max_length=50)
    resource_person = models.CharField(max_length=110)
    resource_person_pic = models.FileField(default='')
    resource_person_data = RichTextUploadingField()

    registered_student = models.IntegerField(default=0)
    registration_open = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
