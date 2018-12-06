from event.models import *
from student.models import *
from .utils import *


# Create your models here.
class RegistrationRecord(models.Model):
    transaction_id = models.SlugField(unique=True)
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=50)
    c_o_e = models.CharField(max_length=75)
    status = models.BooleanField(default=False)
    cancel = models.BooleanField(default=True)
    student = models.ForeignKey(StudentRecord, on_delete=models.CASCADE)
    event = models.ForeignKey(EventRecord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = unique_slug(self, self.event)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id
