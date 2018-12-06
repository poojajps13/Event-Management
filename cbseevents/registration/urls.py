from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('<slug>/register-event', login_required(RegisterEvent.as_view()), name='register_event'),
    path('<slug>/student-list', login_required(RegisterStudentList.as_view()), name='register_student_list'),
    path('<registration_id>/detail', login_required(RegistrationDetail.as_view()), name='registration_detail'),
]
