from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import *


# Create your views here.
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
        except Exception:
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
            if request.user.is_staff:
                obj = EventRecord.objects.get(slug=kwargs['slug'])
                if obj.user == request.user or request.user.is_staff:
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
            if request.user.is_staff:
                obj = EventRecord.objects.get(slug=kwargs['slug'])
                if obj.user == request.user or request.user.is_staff:
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
            else:
                raise PermissionDenied
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('home')


# noinspection PyBroadException
class EventDetail(TemplateView):
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            return render(request, self.template_name, {'obj': obj})
        except Exception:
            messages.error(request, 'Event Not found')
            return redirect('home')
