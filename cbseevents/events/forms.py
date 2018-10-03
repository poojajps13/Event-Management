from django import forms
from django.forms.widgets import SelectDateWidget

from .models import *

EVENTS = [('workshop', 'Workshop'), ('seminar', 'Seminar'), ('competition', 'Competition'), ('training', 'Training'),
          ('guest lecture', 'Guest Lecture'), ]
BRANCHES = [('CSE', 'CSE'), ('IT', 'IT'), ('EC', 'EC'), ('ME', 'ME'), ('EN', 'EN'), ('CE', 'CE'), ('OTHER', 'OTHER'), ]
DATE = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
        (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
        (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30),
        (31, 31), ]
MONTHS = [
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
]
YEARS = [(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), ]
CHOICE = [('YES', 'YES'), ('NO', 'NO'), ]
YEAR = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
SEM = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
class StudentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), required=True, max_length=150)
    email = forms.EmailField(widget=forms.EmailInput(), required=True, max_length=150)
    roll_no = forms.CharField(widget=forms.TextInput(), required=True, max_length=30)
    college_name = forms.CharField(widget=forms.TextInput(), required=True, max_length=200)
    branch = forms.CharField(label='BRANCHES', widget=forms.Select(choices=BRANCHES), required=True)
    year = forms.CharField(label='YEAR', widget=forms.Select(choices=YEAR), required=True)
    sem = forms.CharField(label='SEMESTER', widget=forms.Select(choices=SEM), required=True)
    number = forms.CharField(widget=forms.TextInput(), required=True, max_length=10)

    class Meta:
        model = StudentRecord
        fields = ['name', 'email','roll_no','college_name', 'branch', 'year', 'sem', 'number']


class EventForm(forms.Form):
    select_event = forms.CharField(label='SELECT_EVENT', widget=forms.Select(choices=EVENTS), required=True)
    slug = forms.CharField(widget=forms.TextInput(), required=True, max_length=50)
    event_name = forms.CharField(widget=forms.TextInput(), required=True, max_length=50)
    description = forms.CharField(widget=forms.Textarea(), required=True, max_length=1000)
    duration = forms.CharField(widget=forms.TextInput(), required=True, max_length=20)
    resource_person = forms.CharField(widget=forms.TextInput(), required=True, max_length=50)
    resource_person_data = forms.CharField(widget=forms.Textarea(), required=False, max_length=500)
    registration_start = forms.DateTimeField(widget=SelectDateWidget, required=True)
    registration_end = forms.DateTimeField(widget=SelectDateWidget, required=True)
    event_date = forms.IntegerField(label='DAY', widget=forms.Select(choices=DATE), required=True)
    event_month = forms.CharField(label='MONTH', widget=forms.Select(choices=MONTHS), required=True)
    event_year = forms.IntegerField(label='YEAR', widget=forms.Select(choices=YEARS), required=True)
    eligible_branches = forms.CharField(label='ELIGIBLE BRANCHES',
                                        widget=forms.CheckboxSelectMultiple(choices=BRANCHES), required=True)
    outside_student = forms.CharField(label='OUTSIDE STUDENTS ALLOWED',
                                      widget=forms.RadioSelect(choices=CHOICE), required=True)
    venue = forms.CharField(widget=forms.Textarea(), required=True, max_length=1000)
    fees = forms.FloatField(widget=forms.TextInput(), required=True)
