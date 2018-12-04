from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('<slug>/register-event', login_required(RegisterEvent.as_view()), name='register_event'),
    path('<transaction_id>/detail', login_required(RegistrationDetail.as_view()), name='registration_detail'),
]
