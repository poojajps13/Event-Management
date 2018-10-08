# from .models import WorkshopRecord
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect

from events.models import *


# Create your views here.
def workshop(request):
    workshop_list = WorkshopRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})


def workshop_description(request, slug):
    try:
        workshop = WorkshopRecord.objects.get(slug=slug)
        return render(request, 'description.html', {'obj': workshop, 'event': 'workshop'})
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop Not Found!!!')


def workshop_search(request, year, month):
    workshop_list = WorkshopRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})


def update_workshop(request, slug):
    try:
        event = WorkshopRecord.objects.get(slug=slug)
        if event.user == request.user:
            if request.method == "POST":
                event.event_name = request.POST['event_name']
                event.duration = request.POST['duration']
                event.description = request.POST['description']
                event.resource_person = request.POST['resource_person']
                event.resource_person_data = request.POST['resource_person_data']
                event.registration_start = request.POST['registration_start']
                event.registration_end = request.POST['registration_end']
                event.event_date = request.POST['event_date']
                event.event_month = request.POST['event_month']
                event.event_year = request.POST['event_year']
                event.eligible_branches = request.POST['eligible_branches']
                event.outside_student = request.POST['outside_student']
                event.venue = request.POST['venue']
                event.fees = request.POST['fees']
                event.save(
                    update_fields=['event_name', 'description', 'duration', 'resource_person', 'resource_person_data',
                                   'registration_start', 'registration_end', 'event_date', 'event_month', 'event_year',
                                   'eligible_branches', 'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def delete_workshop(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    try:
        obj = WorkshopRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Workshop deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Workshop does not exist !!!')
    workshop_list = WorkshopRecord.objects.all().order_by('-pk')
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})
