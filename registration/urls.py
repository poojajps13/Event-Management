from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import RegisterEvent, RegistrationDetail, RegisterStudentList
from .views import EnrollmentReport, RegistrationReport, TransactionReport

urlpatterns = [
    path('<slug>/register-event', login_required(RegisterEvent.as_view()), name='register_event'),
    path('<slug>/student-list', login_required(RegisterStudentList.as_view()), name='register_student_list'),
    path('<registration_id>/detail', login_required(RegistrationDetail.as_view()), name='registration_detail'),
    path('<slug>/print-enroll-list', login_required(EnrollmentReport.as_view()), name='print_enroll_list'),
    path('<slug>/print-student-list', login_required(RegistrationReport.as_view()), name='print_student_list'),
    path('<slug>/print-transaction-list', login_required(TransactionReport.as_view()), name='print_transaction_list'),
]
