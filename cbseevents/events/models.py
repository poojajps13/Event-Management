from django.contrib.auth.models import User
from django.db import models
from .utils import get_unique_slug, unique_slug


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
    slug = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
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
    registered = models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_year, self.event_month)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class SeminarRecord(models.Model):
    slug = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
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
    registered = models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_year, self.event_month)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class TrainingRecord(models.Model):
    slug = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
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
    registered = models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_year, self.event_month)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class CompetitionRecord(models.Model):
    slug = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
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
    registered = models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_year, self.event_month)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class GuestLectureRecord(models.Model):
    slug = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
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
    registered = models.IntegerField(default=0)
    fees = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.c_o_e, self.event_year, self.event_month)
        super().save(*args, **kwargs)

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
    registered_event_code = models.CharField(max_length=55)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StudentRecordWorkshop(models.Model):
    name = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='workshop_student')
    registered_event_code = models.CharField(max_length=55)
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.c_o_e)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StudentRecordSeminar(models.Model):
    name = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='seminar_student')
    registered_event_code = models.CharField(max_length=55)
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.c_o_e)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StudentRecordTraining(models.Model):
    name = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='training_student')
    registered_event_code = models.CharField(max_length=55)
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.c_o_e)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StudentRecordCompetition(models.Model):
    name = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='competition_student')
    registered_event_code = models.CharField(max_length=55)
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.c_o_e)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StudentRecordGuestlecture(models.Model):
    name = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='guest_lecture_student')
    registered_event_code = models.CharField(max_length=55)
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.c_o_e)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
