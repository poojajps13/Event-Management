from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from registration.models import RegistrationRecord
from .forms import EventForm
from .models import EventRecord


# Create your views here.
# noinspection PyBroadException
class EventDetail(TemplateView):
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            owner = False
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            if obj.user == request.user or request.user.is_superuser:
                owner = True
            return render(request, self.template_name, {'obj': obj, 'owner': owner, 'now': timezone.now()})
        except ObjectDoesNotExist:
            messages.error(request, 'Event Not found')
            return redirect('home')


# noinspection PyBroadException
class AddEvent(TemplateView):
    template_name = 'add_update_event.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                form = EventForm()
            else:
                raise PermissionDenied
            return render(request, self.template_name, {'form': form})
        except PermissionDenied:
            messages.error(request, 'Permission Denied')
            return redirect('home')

    def post(self, request):
        try:
            if request.user.is_staff:
                form = EventForm(request.POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.user = request.user
                    form.save()
                    messages.success(request, 'Event Added')
                    return redirect('event:event_detail', slug=temp.slug)
                else:
                    messages.error(request, 'Invalid Input')
            else:
                raise PermissionDenied
            return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('home')


# noinspection PyBroadException
class UpdateEvent(TemplateView):
    template_name = 'add_update_event.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff or request.user.is_superuser:
                obj = EventRecord.objects.get(slug=kwargs['slug'])
                if obj.user == request.user or request.user.is_superuser:
                    form = EventForm(instance=obj)
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
            return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('home')

    def post(self, request, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            if obj.user == request.user or request.user.is_superuser:
                form = EventForm(request.POST, instance=obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Event Updated')
                    return redirect('event:event_detail', kwargs['slug'])
                else:
                    messages.error(request, 'Invalid Input')
                return render(request, self.template_name, {'form': form})
            else:
                raise PermissionDenied
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('home')


class DeleteEvent(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            if str(obj.timestamp) == kwargs['timestamp'] and (obj.user == request.user or request.user.is_superuser):
                student = RegistrationRecord.objects.filter(event=obj)
                if student:
                    raise PermissionDenied('Student Registered, You can not delete this event.')
                obj.delete()
                messages.success(request, 'Event Deleted')
            else:
                raise PermissionDenied('Permission Denied')
        except ObjectDoesNotExist:
            messages.error(request, 'Event Not found')
            return redirect('home')
        except PermissionDenied as msg:
            messages.warning(request, msg)
            return redirect('account:consolidated_view_all')
