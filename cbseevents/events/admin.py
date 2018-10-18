from django.contrib import admin
from .models import *

admin.site.register(WorkshopRecord)
admin.site.register(SeminarRecord)
admin.site.register(TrainingRecord)
admin.site.register(CompetitionRecord)
admin.site.register(GuestLectureRecord)
admin.site.register(YearRecord)
admin.site.register(MonthRecordworkshop)
admin.site.register(MonthRecordseminar)
admin.site.register(MonthRecordtraining)
admin.site.register(MonthRecordcompetition)
admin.site.register(MonthRecordguest_lecture)
admin.site.register(StudentRecord)
admin.site.register(StudentRecordWorkshop)
admin.site.register(StudentRecordSeminar)
admin.site.register(StudentRecordTraining)
admin.site.register(StudentRecordCompetition)
admin.site.register(StudentRecordGuestlecture)
# Register your models here.
