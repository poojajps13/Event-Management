from django.contrib.auth.models import User
from django.db import models


class MonthRecordworkshop(models.Model):
    month_code = models.CharField(max_length=10)

    def __str__(self):
        return self.month_code
class MonthRecordseminar(models.Model):
    month_code = models.CharField(max_length=10)

    def __str__(self):
        return self.month_code
class MonthRecordtraining(models.Model):
    month_code = models.CharField(max_length=10)

    def __str__(self):
        return self.month_code
class MonthRecordcompetition(models.Model):
    month_code = models.CharField(max_length=10)

    def __str__(self):
        return self.month_code
class MonthRecordguest_lecture(models.Model):
    month_code = models.CharField(max_length=10)

    def __str__(self):
        return self.month_code

class YearRecord(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


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
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.slug


class SeminarRecord(models.Model):
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
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.slug


class TrainingRecord(models.Model):
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
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.slug


class CompetitionRecord(models.Model):
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
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.slug


class GuestLectureRecord(models.Model):
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
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.slug


class StudentRecord(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    roll_no = models.CharField(max_length=30)
    college_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=10)
    year = models.CharField(max_length=50)
    sem = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    registered_event_code = models.CharField(unique=True, max_length=55)

    def __str__(self):
        return self.name
