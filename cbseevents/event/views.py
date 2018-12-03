from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import *


# Create your views here.
class AddEvent(TemplateView):
    template_name = 'add_event1.html'

    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            form.save()
            messages.success(request, 'Event Added')
        else:
            messages.error(request, 'Invalid Input')
        return render(request, self.template_name, {'form': form})
