from event.models import *


# Create your models here.
class RegistrationRecord(models.Model):
    transaction_id = models.SlugField(unique=True)
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=50)
    c_o_e = models.CharField(max_length=75)
    status = models.BooleanField(default=False)
    cancel = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    event = models.ForeignKey(EventRecord, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id
