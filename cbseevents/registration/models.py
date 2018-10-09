from events.models import *

# Create your models here.
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
    workshop = models.ManyToManyField(WorkshopRecord)
    seminar = models.ManyToManyField(SeminarRecord)
    training = models.ManyToManyField(TrainingRecord)
    competition = models.ManyToManyField(CompetitionRecord)
    guest_lecture = models.ManyToManyField(GuestLectureRecord)

    def __str__(self):
        return self.name
