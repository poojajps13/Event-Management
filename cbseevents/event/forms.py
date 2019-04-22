from datetime import date

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms.widgets import SelectDateWidget

from .models import EventRecord

EVENTS = [('workshop', 'Workshop'), ('seminar', 'Seminar'), ('competition', 'Competition'), ('training', 'Training'),
          ('guest-lecture', 'Guest Lecture')]
BRANCHES = [('CSE', 'CSE'), ('IT', 'IT'), ('EC', 'EC'), ('ME', 'ME'), ('EN', 'EN'),
            ('CE', 'CE'), ('MCA', 'MCA'), ('OTHER', 'OTHER')]
CHOICE = [(1, 'YES'), (0, 'NO')]
CENTER_OF_EXCELLENCE = [('SDA', 'Structural Design And Analysis'),
                        ('NW', 'Cisco Networking Academy'),
                        ('TIES', 'Texas Instruments Embedded System Lab'),
                        ('SMC', 'SMC India Pvt Ltd.'),
                        ('IARTC', 'Industrial Automation Research And Training Centre - IARTC'),
                        ('VLSI', 'VLSI Design'),
                        ('BIGD', 'Big Data Analytics'),
                        ('MobApp', 'Mobile Application Development'),
                        ('SWD', 'Center For Enterprise Software Development'),
                        ('TST', 'Testing'),
                        ('NI', 'ABES-NI Innovation Centre')]
DURATION_STRING = [('Hour', 'Hour'), ('Day', 'Day'), ('Week', 'Week'), ('Month', 'Month')]


class EventForm(forms.ModelForm):
    type = forms.CharField(widget=forms.Select(
        choices=EVENTS, attrs={'class': 'form-control'}), required=True)
    c_o_e = forms.CharField(widget=forms.Select(
        choices=CENTER_OF_EXCELLENCE, attrs={'class': 'form-control'}), required=True)

    event_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Event Name'}), required=True, max_length=100)
    event_pic = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1", 'accept': '.pdf'}), required=True)
    fees = forms.FloatField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Fees'}), required=True)
    registration_start = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    registration_end = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    event_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    duration_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Durations'}), required=True, max_length=5)
    duration_string = forms.CharField(widget=forms.Select(
        choices=DURATION_STRING, attrs={'class': 'form-control'}), required=True)
    eligible_branches = forms.CharField(widget=forms.CheckboxSelectMultiple(
        choices=BRANCHES, attrs={'class': 'form-check-inline'}), required=True)

    pre_requisites_1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Pre Requisites'}), required=True, max_length=50)
    pre_requisites_2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Pre Requisites'}), required=True, max_length=50)
    pre_requisites_3 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Pre Requisites'}), required=True, max_length=50)
    learning_outcome_1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Learning Outcome'}), required=True, max_length=50)
    learning_outcome_2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Learning Outcome'}), required=True, max_length=50)
    learning_outcome_3 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Learning Outcome'}), required=True, max_length=50)
    learning_outcome_4 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Learning Outcome'}), required=True, max_length=50)
    learning_outcome_5 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Learning Outcome'}), required=True, max_length=50)
    learning_outcome_6 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Learning Outcome'}), required=True, max_length=50)
    description = forms.CharField(widget=CKEditorUploadingWidget())

    outside_student = forms.IntegerField(widget=forms.RadioSelect(
        choices=CHOICE, attrs={'class': 'form-check-inline'}), required=True)
    venue = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Venue'}), required=True, max_length=50)
    resource_person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Resource Person'}), required=True, max_length=100)
    resource_person_data = forms.CharField(widget=CKEditorUploadingWidget())
    resource_person_pic = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1", 'accept': '.pdf'}), required=True)

    class Meta:
        model = EventRecord
        fields = ['event_name', 'description', 'duration_number', 'resource_person', 'resource_person_data', 'venue',
                  'fees', 'registration_start', 'registration_end', 'event_date', 'type', 'c_o_e', 'duration_string',
                  'eligible_branches', 'outside_student', 'pre_requisites_1', 'pre_requisites_2', 'pre_requisites_3',
                  'learning_outcome_1', 'learning_outcome_2', 'learning_outcome_3', 'learning_outcome_4',
                  'learning_outcome_5', 'learning_outcome_6', 'resource_person_pic', 'event_pic']

    def clean_registration_start(self):
        try:
            registration_start = self.cleaned_data['registration_start']
            if True or registration_start.strftime('%Y-%m-%d') >= date.today().strftime('%Y-%m-%d'):
                return registration_start
            raise forms.ValidationError("Invalid Start Date")
        except Exception:
            raise forms.ValidationError("Invalid Start Date")

    def clean_registration_end(self):
        try:
            registration_start = self.cleaned_data['registration_start']
            registration_end = self.cleaned_data['registration_end']
            if registration_start <= registration_end:
                return registration_end
            raise forms.ValidationError("Invalid End Date")
        except Exception:
            raise forms.ValidationError("Invalid End Date")

    def clean_event_date(self):
        try:
            registration_start = self.cleaned_data['registration_start']
            event_date = self.cleaned_data['event_date']
            if registration_start <= event_date:
                return event_date
            raise forms.ValidationError("Invalid Event Date")
        except Exception:
            raise forms.ValidationError("Invalid Event Date")

    def clean_fees(self):
        fee = self.cleaned_data['fees']
        if 0 <= fee <= 10000:
            return fee
        raise forms.ValidationError('Invalid Amount')
