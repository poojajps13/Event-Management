from datetime import date

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import *


# Create your views here.
# noinspection PyBroadException
class RegisterEvent(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.is_staff:
                obj = EventRecord.objects.get(slug=kwargs['slug'])
                t = date.today().strftime('%Y-%m-%d')
                if (obj.registration_start.strftime('%Y-%m-%d') <= t) and (
                        t <= obj.registration_end.strftime('%Y-%m-%d')):
                    student = StudentRecord.objects.get(user=request.user)
                    try:
                        RegistrationRecord.objects.get(student=student, event=obj)
                        messages.warning(request, 'Already Registered')
                    except ObjectDoesNotExist:
                        RegistrationRecord.objects.create(student=student, event=obj, c_o_e=obj.c_o_e, type=obj.type)
                        obj.registered_student += 1
                        obj.save(update_fields=['registered_student'])
                        messages.success(request, 'Successfully Registered')
                else:
                    messages.error(request, 'Registration Closed')
            else:
                raise PermissionDenied
            return redirect('event:event_detail', kwargs['slug'])
        except ObjectDoesNotExist:
            messages.error(request, 'Record Not Found')
            return redirect('home')
        except PermissionDenied:
            messages.warning(request, 'You have not Permission to Register')
        except Exception:
            messages.error(request, 'Try After Some Time')
            return redirect('home')


# noinspection PyBroadException
class RegisterStudentList(TemplateView):
    template_name = 'register_student_list.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                obj = RegistrationRecord.objects.filter(event=event)
                return render(request, self.template_name, {'obj': obj})
            raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')


# noinspection PyBroadException
class RegistrationDetail(TemplateView):
    template_name = 'registration_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(registration_id=kwargs['registration_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                form = TransactionForm()
                return render(request, self.template_name, {'obj': obj, 'form': form, 'staff': True})
            student = StudentRecord.objects.get(user=request.user)
            if student == obj.student:
                return render(request, self.template_name, {'obj': obj, 'staff': False})
            raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')

    def post(self, request, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(registration_id=kwargs['registration_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                form = TransactionForm(request.POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.registration_id = obj.registration_id
                    obj.amount += temp.amount
                    temp.save()
                    obj.save(update_fields=['amount'])
                    obj.transaction_id.add(temp)
                    messages.success(request, 'Successfully Update')
                    return redirect('registration:registration_detail', kwargs['slug'])
                else:
                    messages.error(request, 'Invalid Inputs')
                    return render(request, self.template_name, {'obj': obj, 'form': form, 'staff': True})
            else:
                raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
