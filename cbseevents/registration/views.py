from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import *


def event_registration(request, slug, event):
    if event == 'workshop':
        obj = WorkshopRecord.objects.get(slug=slug)
    elif event == 'seminar':
        obj = SeminarRecord.objects.get(slug=slug)
    elif event == 'training':
        obj = TrainingRecord.objects.get(slug=slug)
    elif event == 'competition':
        obj = CompetitionRecord.objects.get(slug=slug)
    else:
        obj = GuestLectureRecord.objects.get(slug=slug)
    if True:
        if obj.registration_end.strftime('%Y-%m-%d') > date.today().strftime('%Y-%m-%d'):
            if request.method == "POST":
                form = StudentForm(request.POST)
                if True:
                    if form.is_valid():
                        obj1 = form.save()
                        obj.registered = obj.registered + 1
                        obj.save(update_fields=['registered'])
                        if event == 'workshop':
                            obj1.workshop.add(obj)
                        elif event == 'seminar':
                            obj1.seminar.add(obj)
                        elif event == 'training':
                            obj1.training.add(obj)
                        elif event == 'competition':
                            obj1.competition.add(obj)
                        else:
                            obj1.guest_lecture.add(obj)
                        messages.success(request, 'Successfully Registered')
                    else:
                        messages.error(request, 'Invalid form')
                # except Exception:
                #     messages.error(request, 'Try again')
                form = StudentForm()
                return render(request, 'studentform.html', {'form': form})
            else:
                form = StudentForm()
            return render(request, 'studentform.html', {'form': form})
        else:
            messages.error(request, 'REGISTRATION CLOSED')
    # except Exception:
    #     messages.error(request, 'Try Later')
    return redirect('home')
