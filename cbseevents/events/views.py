from datetime import date

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import *
from .models import *


def home(request):
    work = WorkshopRecord.objects.all().order_by('-pk')
    semi = SeminarRecord.objects.all().order_by('-pk')
    train = TrainingRecord.objects.all().order_by('-pk')
    comp = CompetitionRecord.objects.all().order_by('-pk')
    guest = GuestLectureRecord.objects.all().order_by('-pk')
    return render(request, 'index.html', {'work': work, 'semi': semi, 'train': train, 'comp': comp, 'guest': guest})


def workshop(request):
    workshop_list = WorkshopRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordworkshop.objects.all()
    return render(request, 'workshop.html',
                  {'event_list': workshop_list, 'year_list': year_list, 'months_list': months_list})


def workshop_description(request, slug):
    workshop = WorkshopRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': workshop, 'event': 'workshop'})


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
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def workshop_registration(request, slug, c_o_e):
    obj = WorkshopRecord.objects.get(slug=slug)
    try:
        if obj.registration_end.strftime('%Y-%m-%d') > date.today().strftime('%Y-%m-%d'):
            if request.method == "POST":
                form = StudentForm(request.POST)
                try:
                    if form.is_valid():
                        name = form.cleaned_data['name']
                        email = form.cleaned_data['email']
                        roll_no = form.cleaned_data['roll_no']
                        college_name = form.cleaned_data['college_name']
                        branch = form.cleaned_data['branch']
                        year = form.cleaned_data['year']
                        sem = form.cleaned_data['sem']
                        number = form.cleaned_data['number']
                        password = form.cleaned_data['password']
                        obj.registered = obj.registered + 1
                        obj.save(update_fields=['registered'])
                        WorkshopStudent.objects.create(name=name, email=email, roll_no=roll_no, college_name=college_name,
                                             branch=branch, year=year, sem=sem, number=number,
                                             password=password,registered_event_code=slug)
                        StudentRecordWorkshop.objects.create(name=name,registered_event_code=slug,c_o_e=c_o_e)
                        messages.success(request, 'Successfully Registered')
                    else:
                        messages.error(request, 'Invalid form')
                except Exception:
                    messages.error(request, 'Try again')
                return render(request, 'studentform.html', {'form': form})
            else:
                form = StudentForm()
            return render(request, 'studentform.html', {'form': form})
        else:
            messages.error(request, 'REGISTRATION CLOSED')
    except Exception:
        messages.error(request, 'Try Later')
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


def seminar(request):
    seminar_list = SeminarRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordseminar.objects.all()
    return render(request, 'seminar.html',
                  {'event_list': seminar_list, 'year_list': year_list, 'months_list': months_list})


def seminar_description(request, slug):
    seminar = SeminarRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': seminar, 'event': 'seminar'})


def seminar_search(request, year, month):
    seminar_list = SeminarRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordseminar.objects.all()
    return render(request, 'seminar.html',
                  {'event_list': seminar_list, 'year_list': year_list, 'months_list': months_list})


def update_seminar(request, slug):
    try:
        event = SeminarRecord.objects.get(slug=slug)
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
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Seminar does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def seminar_registration(request, slug, c_o_e):
    obj = SeminarRecord.objects.get(slug=slug)
    try:
        if obj.registration_end.strftime('%Y-%m-%d') > date.today().strftime('%Y-%m-%d'):
            if request.method == "POST":
                form = StudentForm(request.POST)
                try:
                    if form.is_valid():
                        name = form.cleaned_data['name']
                        email = form.cleaned_data['email']
                        roll_no = form.cleaned_data['roll_no']
                        college_name = form.cleaned_data['college_name']
                        branch = form.cleaned_data['branch']
                        year = form.cleaned_data['year']
                        sem = form.cleaned_data['sem']
                        number = form.cleaned_data['number']
                        password = form.cleaned_data['password']
                        obj.registered = obj.registered + 1;
                        obj.save(update_fields=['registered'])
                        SeminarStudent.objects.create(name=name, email=email, roll_no=roll_no, college_name=college_name,
                                                     branch=branch,password=password,
                                                     year=year, sem=sem, number=number, registered_event_code=slug)
                        StudentRecordSeminar.objects.create(name=name,registered_event_code=slug,c_o_e=c_o_e)
                        messages.success(request, 'Successfully Registered')
                    else:
                        messages.error(request, 'Invalid form')
                except Exception:
                    messages.error(request, 'Try again')
                form = StudentForm()
                return render(request, 'studentform.html', {'form': form})
            else:
                form = StudentForm()
            return render(request, 'studentform.html', {'form': form})
        else:
            messages.error(request, 'REGISTRATION CLOSED')
    except Exception:
        messages.error(request, 'Registration Closed')
    return redirect('home')


def delete_seminar(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordseminar.objects.all()
    try:
        obj = SeminarRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Seminar deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Seminar does not exist')
    except PermissionDenied:
        messages.error(request, 'Seminar does not exist !!!')
    seminar_list = SeminarRecord.objects.all().order_by('-pk')
    return render(request, 'seminar.html',
                  {'event_list': seminar_list, 'year_list': year_list, 'months_list': months_list})


def training(request):
    training_list = TrainingRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordtraining.objects.all()
    return render(request, 'training.html',
                  {'event_list': training_list, 'year_list': year_list, 'months_list': months_list})


def training_description(request, slug):
    training = TrainingRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': training, 'event': 'training'})


def training_search(request, year, month):
    training_list = TrainingRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordtraining.objects.all()
    return render(request, 'training.html',
                  {'event_list': training_list, 'year_list': year_list, 'months_list': months_list})


def update_training(request, slug):
    try:
        event = TrainingRecord.objects.get(slug=slug)
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
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Training does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def training_registration(request, slug, c_o_e):
    obj = TrainingRecord.objects.get(slug=slug)
    try:
        if obj.registration_end.strftime('%Y-%m-%d') > date.today().strftime('%Y-%m-%d'):
            if request.method == "POST":
                form = StudentForm(request.POST)
                try:
                    if form.is_valid():
                        name = form.cleaned_data['name']
                        email = form.cleaned_data['email']
                        roll_no = form.cleaned_data['roll_no']
                        college_name = form.cleaned_data['college_name']
                        branch = form.cleaned_data['branch']
                        year = form.cleaned_data['year']
                        sem = form.cleaned_data['sem']
                        number = form.cleaned_data['number']
                        password = form.cleaned_data['password']
                        obj.registered = obj.registered + 1;
                        obj.save(update_fields=['registered'])
                        TrainingStudent.objects.create(name=name, email=email, roll_no=roll_no, college_name=college_name,
                                                     branch=branch, year=year, sem=sem, number=number,
                                                     password=password,registered_event_code=slug)
                        StudentRecordTraining.objects.create(name=name,registered_event_code=slug,c_o_e=c_o_e)
                        messages.success(request, 'Successfully Registered')
                    else:
                        messages.error(request, 'Invalid form')
                except Exception:
                    messages.error(request, 'Try again')
                form = StudentForm()
                return render(request, 'studentform.html', {'form': form})
            else:
                form = StudentForm()
            return render(request, 'studentform.html', {'form': form})
        else:
            messages.error(request, 'REGISTRATION CLOSED')
    except Exception:
        messages.error(request, 'Registration Closed')
    return redirect('home')


def delete_training(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordtraining.objects.all()
    try:
        obj = TrainingRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Training deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Training does not exist')
    except PermissionDenied:
        messages.error(request, 'Training does not exist !!!')
    training_list = TrainingRecord.objects.all().order_by('-pk')
    return render(request, 'training.html',
                  {'event_list': training_list, 'year_list': year_list, 'months_list': months_list})


def competition(request):
    competition_list = CompetitionRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordcompetition.objects.all()
    return render(request, 'competition.html',
                  {'event_list': competition_list, 'year_list': year_list, 'months_list': months_list})


def competition_description(request, slug):
    competition = CompetitionRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': competition, 'event': 'competition'})


def competition_search(request, year, month):
    competition_list = CompetitionRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordcompetition.objects.all()
    return render(request, 'competition.html',
                  {'event_list': competition_list, 'year_list': year_list, 'months_list': months_list})


def update_competition(request, slug):
    try:
        event = CompetitionRecord.objects.get(slug=slug)
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
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Permission Denied')
    return redirect('home')


def competition_registration(request, slug, c_o_e):
    obj = CompetitionRecord.objects.get(slug=slug)
    try:
        if obj.registration_end.strftime('%Y-%m-%d') > date.today().strftime('%Y-%m-%d'):
            if request.method == "POST":
                form = StudentForm(request.POST)
                try:
                    if form.is_valid():
                        name = form.cleaned_data['name']
                        email = form.cleaned_data['email']
                        roll_no = form.cleaned_data['roll_no']
                        college_name = form.cleaned_data['college_name']
                        branch = form.cleaned_data['branch']
                        year = form.cleaned_data['year']
                        sem = form.cleaned_data['sem']
                        number = form.cleaned_data['number']
                        password = form.cleaned_data['password']
                        obj.registered = obj.registered + 1;
                        obj.save(update_fields=['registered'])
                        CompetitionStudent.objects.create(name=name, email=email, roll_no=roll_no, college_name=college_name,
                                                     branch=branch, year=year, sem=sem, number=number,
                                                     password=password,registered_event_code=slug)
                        StudentRecordCompetition.objects.create(name=name,registered_event_code=slug,c_o_e=c_o_e)
                        messages.success(request, 'Successfully Registered')
                    else:
                        messages.error(request, 'Invalid form')
                except Exception:
                    messages.error(request, 'Try again')
                form = StudentForm()
                return render(request, 'studentform.html', {'form': form})
            else:
                form = StudentForm()
            return render(request, 'studentform.html', {'form': form})
        else:
            messages.error(request, 'REGISTRATION CLOSED')
    except Exception:
        messages.error(request, 'Registration Closed')
    return redirect('home')


def delete_competition(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordcompetition.objects.all()
    try:
        obj = CompetitionRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Workshop deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Competition does not exist')
    except PermissionDenied:
        messages.error(request, 'Competition does not exist !!!')
    competition_list = CompetitionRecord.objects.all().order_by('-pk')
    return render(request, 'competition.html',
                  {'event_list': competition_list, 'year_list': year_list, 'months_list': months_list})


def guest_lecture(request):
    guest_lecture_list = GuestLectureRecord.objects.all().order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordguest_lecture.objects.all()
    print(year_list, months_list)
    return render(request, 'guest_lecture.html',
                  {'event_list': guest_lecture_list, 'year_list': year_list, 'months_list': months_list})


def guest_lecture_description(request, slug):
    guest_lecture = GuestLectureRecord.objects.get(slug=slug)
    return render(request, 'description.html', {'obj': guest_lecture, 'event': 'guest_lecture'})


def guest_lecture_search(request, year, month):
    guest_lecture_list = GuestLectureRecord.objects.filter(event_year=year, event_month=month).order_by('-pk')
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordguest_lecture.objects.all()
    return render(request, 'guest_lecture.html',
                  {'event_list': guest_lecture_list, 'year_list': year_list, 'months_list': months_list})


def update_guestlecture(request, slug):
    try:
        event = GuestLectureRecord.objects.get(slug=slug)
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
                                   'eligible_branches',
                                   'outside_student', 'venue', 'fees'])
            return render(request, 'update.html', {'event': event})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Workshop does not exist')
    except PermissionDenied:
        messages.error(request, 'Workshop does not exist !!!')
    return render(request, 'update.html')


def guest_lecture_registration(request, slug, c_o_e):
    obj = GuestLectureRecord.objects.get(slug=slug)
    try:
        if obj.registration_end.strftime('%Y-%m-%d') > date.today().strftime('%Y-%m-%d'):
            if request.method == "POST":
                form = StudentForm(request.POST)
                try:
                    if form.is_valid():
                        name = form.cleaned_data['name']
                        email = form.cleaned_data['email']
                        roll_no = form.cleaned_data['roll_no']
                        college_name = form.cleaned_data['college_name']
                        branch = form.cleaned_data['branch']
                        year = form.cleaned_data['year']
                        sem = form.cleaned_data['sem']
                        number = form.cleaned_data['number']
                        password = form.cleaned_data['password']
                        obj.registered = obj.registered + 1
                        obj.save(update_fields=['registered'])
                        GuestlectureStudent.objects.create(name=name, email=email, roll_no=roll_no, college_name=college_name,
                            branch=branch, year=year, sem=sem, number=number,password=password,registered_event_code=slug)
                        StudentRecordGuestlecture.objects.create(name=name,registered_event_code=slug,c_o_e=c_o_e)
                        messages.success(request, 'Successfully Registered')
                        return redirect('home')
                    else:
                        messages.error(request, 'Invalid form')
                except Exception:
                    messages.error(request, 'Try again')
                return render(request, 'studentform.html', {'form': form})
            else:
                form = StudentForm()
            return render(request, 'studentform.html', {'form': form})
        else:
            messages.error(request, 'REGISTRATION CLOSED')
    except Exception:
        messages.error(request, 'Registration Closed')
    return redirect('home')


def delete_guestlecture(request, slug):
    year_list = YearRecord.objects.all().order_by('-year')
    months_list = MonthRecordguest_lecture.objects.all()
    try:
        obj = GuestLectureRecord.objects.get(slug=slug)
        if obj.user == request.user:
            obj.delete()
            messages.success(request, 'Guest Lecture deleted')
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Guest Lecture does not exist')
    except PermissionDenied:
        messages.error(request, 'Guest Lecture  does not exist !!!')
    guestlecture_list = GuestLectureRecord.objects.all().order_by('-pk')
    return render(request, 'guest_lecture.html',
                  {'event_list': guestlecture_list, 'year_list': year_list, 'months_list': months_list})


def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if True:
            if form.is_valid():
                select_event = form.cleaned_data['select_event']
                c_o_e = form.cleaned_data['c_o_e']
                event_name = form.cleaned_data['event_name']
                description = form.cleaned_data['description']
                duration = form.cleaned_data['duration']
                resource_person = form.cleaned_data['resource_person']
                resource_person_data = form.cleaned_data['resource_person_data']
                registration_start = form.cleaned_data['registration_start']
                registration_end = form.cleaned_data['registration_end']
                event_date = form.cleaned_data['event_date']
                event_month = form.cleaned_data['event_month']
                event_year = form.cleaned_data['event_year']
                eligible_branches = form.cleaned_data['eligible_branches']
                outside_student = form.cleaned_data['outside_student']
                venue = form.cleaned_data['venue']
                fees = form.cleaned_data['fees']
                if select_event == 'workshop':
                    WorkshopRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                  description=description, resource_person=resource_person,
                                                  resource_person_data=resource_person_data,
                                                  registration_start=registration_start,
                                                  registration_end=registration_end,
                                                  event_date=event_date, event_month=event_month, event_year=event_year,
                                                  eligible_branches=eligible_branches,
                                                  outside_student=outside_student, venue=venue, fees=fees,
                                                  user=request.user)
                if select_event == 'seminar':
                    SeminarRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                 description=description, resource_person=resource_person,
                                                 resource_person_data=resource_person_data,
                                                 registration_start=registration_start,
                                                 registration_end=registration_end,
                                                 event_date=event_date, event_month=event_month, event_year=event_year,
                                                 eligible_branches=eligible_branches,
                                                 outside_student=outside_student, venue=venue, fees=fees,
                                                 user=request.user)
                if select_event == 'training':
                    TrainingRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                  description=description, resource_person=resource_person,
                                                  resource_person_data=resource_person_data,
                                                  registration_start=registration_start,
                                                  registration_end=registration_end,
                                                  event_date=event_date, event_month=event_month, event_year=event_year,
                                                  eligible_branches=eligible_branches,
                                                  outside_student=outside_student, venue=venue, fees=fees,
                                                  user=request.user)
                if select_event == 'competition':
                    CompetitionRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                     description=description, resource_person=resource_person,
                                                     resource_person_data=resource_person_data,
                                                     registration_start=registration_start,
                                                     registration_end=registration_end,
                                                     event_date=event_date, event_month=event_month,
                                                     event_year=event_year,
                                                     eligible_branches=eligible_branches,
                                                     outside_student=outside_student, venue=venue, fees=fees,
                                                     user=request.user)
                if select_event == 'guest lecture':
                    GuestLectureRecord.objects.create(c_o_e=c_o_e, event_name=event_name, duration=duration,
                                                      description=description, resource_person=resource_person,
                                                      resource_person_data=resource_person_data,
                                                      registration_start=registration_start,
                                                      registration_end=registration_end,
                                                      event_date=event_date, event_month=event_month,
                                                      event_year=event_year,
                                                      eligible_branches=eligible_branches,
                                                      outside_student=outside_student, venue=venue, fees=fees,
                                                      user=request.user)
                try:
                    YearRecord.objects.get(year=event_year)
                except ObjectDoesNotExist:
                    YearRecord.objects.create(year=event_year)
                if select_event == 'workshop':
                    try:
                        MonthRecordworkshop.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordworkshop.objects.create(month_code=event_month)
                if select_event == 'training':
                    try:
                        MonthRecordtraining.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordtraining.objects.create(month_code=event_month)
                if select_event == 'seminar':
                    try:
                        MonthRecordseminar.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordseminar.objects.create(month_code=event_month)
                if select_event == 'competition':
                    try:
                        MonthRecordcompetition.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordcompetition.objects.create(month_code=event_month)
                if select_event == 'guest lecture':
                    try:
                        MonthRecordguest_lecture.objects.get(month_code=event_month)
                    except ObjectDoesNotExist:
                        MonthRecordguest_lecture.objects.create(month_code=event_month)
                    messages.success(request, 'Successfully added Event')
            else:
                messages.error(request, 'Invalid form')
        #except Exception:
           # messages.error(request, 'Try again')
        return render(request, 'add_event.html', {'form': form})
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def add_user(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'add_user.html', {'form': form})
    return redirect('superuser')


def edit_user(request, username):
    try:
        u = User.objects.get(username=username)
        if request.user.is_staff:
            if request.method == "POST":
                u.Username = request.POST['username']
                new_password = request.POST['password']
                u.set_password(new_password)
                u.save(update_fields=['username', 'password'])
            return render(request, 'edit_user.html', {'u': u})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    except PermissionDenied:
        messages.error(request, 'User does not exist !!!')
    return render(request, 'edit_user.html', {'u': u})


def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")
    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'superuser.html')
    except Exception as e:
        return render(request, 'superuser.html', {'err': e.message})
    return redirect('superuser')


def consolidated(request, username):
    user = User.objects.get(username=username)
    workshop = WorkshopRecord.objects.filter(user=user)
    seminar = SeminarRecord.objects.filter(user=user)
    training = TrainingRecord.objects.filter(user=user)
    competition = CompetitionRecord.objects.filter(user=user)
    guest_lecture = GuestLectureRecord.objects.filter(user=user)
    return render(request, 'consolidatedview.html',
                  {'workshop': workshop, 'training': training, 'competition': competition,
                   'seminar': seminar, 'guest_lecture': guest_lecture, 'now': timezone.now()})


def superuser(request):
    u = User.objects.all()
    return render(request, 'superuser.html', {'u': u})


def logout(request):
    auth.logout(request)
    return redirect('home')


def consolidatedview(request):
    workshop = WorkshopRecord.objects.filter(user=request.user)
    seminar = SeminarRecord.objects.filter(user=request.user)
    training = TrainingRecord.objects.filter(user=request.user)
    competition = CompetitionRecord.objects.filter(user=request.user)
    guest_lecture = GuestLectureRecord.objects.filter(user=request.user)
    return render(request, 'consolidatedview.html',
                  {'workshop': workshop, 'training': training, 'competition': competition,
                   'seminar': seminar, 'guest_lecture': guest_lecture, 'now': timezone.now()})

def studentlist(request,registered_event_code):
    lists = StudentRecordWorkshop.objects.filter(registered_event_code=registered_event_code)
    return render(request,'studentlist.html',{'lists':lists})
    
def excellence_center(request):
    return render(request, 'excellence_center.html')


def structural_design(request):
    return render(request, 'static1.html')


def cisco_networking_academy(request):
    return render(request, 'static2.html')


def texas(request):
    return render(request, 'static3.html')


def smc_india(request):
    return render(request, 'static4.html')


def automation_research(request):
    return render(request, 'static5.html')


def vlsi_design(request):
    return render(request, 'static6.html')


def big_data(request):
    return render(request, 'static7.html')


def innovation_centre(request):
    return render(request, 'static8.html')


def mobile_application(request):
    return render(request, 'static9.html')


def software_development(request):
    return render(request, 'static10.html')
