from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('register-event', login_required(RegisterEvent.as_view()), name='register_event'),
    path('registration-detail', login_required(RegistrationDetail.as_view()), name='registration_detail'),
]
