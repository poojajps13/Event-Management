from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class StudentRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=30)
    college_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=10)
    batch_start = models.CharField(max_length=10)
    batch_end = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
