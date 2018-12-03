from django.urls import path
from .views import *

urlpatterns = [
    path('add-event', AddEvent.as_view(), name='add_event'),
]