from django.contrib import messages
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
                RegistrationRecord.objects.create(user=request.user, event=obj, c_o_e=obj.c_o_e, type=obj.type)
                messages.success(request, 'Successfully Registered')
            else:
                raise PermissionError
        except Exception:
            messages.error(request, 'Try After Some Time')
            return redirect('home')


# noinspection PyBroadException
class RegistrationDetail(TemplateView):
    template_name = 'registration_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(transaction_id=kwargs['transaction_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                return render(request, self.template_name, {'obj': obj, 'staff':True})
            if request.user == obj.user:
                return render(request, self.template_name, {'obj': obj, 'staff':False})
            raise PermissionError
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
                return redirect('registration:registration_detail', kwargs)
            raise PermissionError
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
