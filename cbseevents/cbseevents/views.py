from datetime import date

from django.shortcuts import render, redirect

from event.models import *
from student.models import *


def home(request):
    event_list = EventRecord.objects.all().order_by('-pk')
    return render(request, 'index.html', {'event_list': event_list})


def set_user(request):
    if request.user.is_superuser:
        obj_list = StudentRecord.objects.all()
        for obj in obj_list:
            if obj.user.is_active:
                pass
            else:
                user = obj.user
                # obj.delete()
                # user.delete()
        return redirect('home')
    else:
        return redirect('home')
