from account.models import *
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


class StudentRecordWorkshop(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_student')
    registered_event_code = models.ForeignKey(WorkshopRecord, on_delete=models.CASCADE, related_name='workshop_event')
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
    paid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.registered_event_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class StudentRecordSeminar(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seminar_student')
    registered_event_code = models.ForeignKey(SeminarRecord, on_delete=models.CASCADE, related_name='seminar_event')
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
    paid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.registered_event_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class StudentRecordTraining(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_student')
    registered_event_code = models.ForeignKey(TrainingRecord, on_delete=models.CASCADE, related_name='training_event')
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
    paid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.registered_event_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class StudentRecordCompetition(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competition_student')
    registered_event_code = models.ForeignKey(CompetitionRecord, on_delete=models.CASCADE, related_name='competition')
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
    paid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.registered_event_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class StudentRecordGuestLecture(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_student')
    registered_event_code = models.ForeignKey(GuestLectureRecord, on_delete=models.CASCADE, related_name='guest_event')
    payment_id = models.SlugField(unique=True)
    c_o_e = models.CharField(max_length=75)
    paid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = unique_slug(self, self.registered_event_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
