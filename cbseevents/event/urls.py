from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('add-event', login_required(AddEvent.as_view()), name='add_event'),
    path('<slug>/update-event', login_required(UpdateEvent.as_view()), name='update_event'),
    path('<slug>/event_detail', EventDetail.as_view(), name='event_detail'),
]
