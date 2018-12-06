from datetime import date

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import *


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
        # except Exception:
        #     messages.error(request, 'Try After Some Time')
        #     return redirect('home')


# noinspection PyBroadException
class RegistrationDetail(TemplateView):
    template_name = 'registration_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(transaction_id=kwargs['transaction_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                return render(request, self.template_name, {'obj': obj, 'staff': True})
            student = StudentRecord.objects.get(user=request.user)
            if student == obj.student:
                return render(request, self.template_name, {'obj': obj, 'staff': False})
            raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')

    def post(self, request, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(transaction_id=kwargs['transaction_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                obj.amount = request.POST['amount']
                obj.save(update_fields=['amount'])
                messages.success(request, 'Successfully Update')
            else:
                raise PermissionDenied
            return redirect('registration:registration_detail', kwargs['slug'])
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
