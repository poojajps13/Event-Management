from django import forms
from django.forms.widgets import SelectDateWidget

EVENTS = [('workshop', 'Workshop'), ('seminar', 'Seminar'), ('competition', 'Competition'), ('training', 'Training'),
          ('guest lecture', 'Guest Lecture'), ]
BRANCHES = [('CSE', 'CSE'), ('IT', 'IT'), ('EC', 'EC'), ('ME', 'ME'), ('EN', 'EN'), ('CE', 'CE'), ('OTHER', 'OTHER'), ]
DATE = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
        (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
        (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30),
        (31, 31), ]
MONTHS = [
    ('Jan', 'January'),
    ('Feb', 'February'),
    ('Mar', 'March'),
    ('Apr', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('Aug', 'August'),
    ('Sep', 'September'),
    ('Oct', 'October'),
    ('Nov', 'November'),
    ('Dec', 'December'),
]
YEARS = [(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), ]
CHOICE = [('YES', 'YES'), ('NO', 'NO'), ]
CENTER_OF_EXCELLENCE = [('SDA', 'Structural Design And Analysis'),
                        ('NW', 'Cisco Networking Academy'),
                        ('TIES', 'Texas Instruments Embedded System Lab'),
                        ('SMC', 'SMC India Pvt Ltd.'),
                        ('IARTC', 'Industrial Automation Research And Training Centre - IARTC'),
                        ('VLSI', 'VLSI Design'),
                        ('BigD', 'Big Data Analytics'),
                        ('MobApp', 'Mobile Application Development'),
                        ('SWD', 'Center For Enterprise Software Development'),
                        ('TST', 'Testing'),
                        ('NI', 'ABES-NI Innovation Centre'),
                        ]


class EventForm(forms.Form):
    select_event = forms.CharField(label='SELECT_EVENT',
                                   widget=forms.Select(choices=EVENTS, attrs={'class': 'form-control'}), required=True)
    c_o_e = forms.CharField(
        label='CENTER_OF_EXCELLENCE', widget=forms.Select(
            choices=CENTER_OF_EXCELLENCE, attrs={'class': 'form-control'}), required=True, max_length=50)
    event_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
                                 required=True, max_length=100)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '4'}),
        required=True, max_length=2000)
    duration = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration'}),
                               required=True, max_length=20)
    resource_person = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource Person'}), required=True,
        max_length=100)
    resource_person_data = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
                                           required=False, max_length=2000)
    registration_start = forms.DateTimeField(widget=SelectDateWidget(attrs={'class': 'form-control my-2'}),
                                             required=True)
    registration_end = forms.DateTimeField(widget=SelectDateWidget(attrs={'class': 'form-control my-2'}),
                                           required=True)
    event_date = forms.IntegerField(label='DAY',
                                    widget=forms.Select(choices=DATE, attrs={'class': 'form-control my-2'}),
                                    required=True)
    event_month = forms.CharField(label='MONTH',
                                  widget=forms.Select(choices=MONTHS, attrs={'class': 'form-control my-2'}),
                                  required=True)
    event_year = forms.IntegerField(label='YEAR',
                                    widget=forms.Select(choices=YEARS, attrs={'class': 'form-control my-2'}),
                                    required=True)
    eligible_branches = forms.CharField(
        label='ELIGIBLE BRANCHES', widget=forms.CheckboxSelectMultiple(
            choices=BRANCHES, attrs={'class': 'form-check-inline'}), required=True)
    outside_student = forms.CharField(
        label='OUTSIDE STUDENTS ALLOWED',
        widget=forms.RadioSelect(choices=CHOICE, attrs={'class': 'form-check-inline'}),
        required=True)
    venue = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Venue', 'rows': '4'}),
                            required=True, max_length=2000)
    fees = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fees'}),
                            required=True)
