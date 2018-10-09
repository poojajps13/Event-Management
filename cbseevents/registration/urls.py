from django.urls import path

from .views import *

urlpatterns = [
    path('<event>/<slug>', event_registration, name='event_registration'),
]
