from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import StudentRecord

BATCH_START = [('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'),
               ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')]
BATCH_END = [('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'),
             ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')]
BRANCHES = [('CSE', 'CSE'), ('IT', 'IT'), ('EC', 'EC'), ('ME', 'ME'), ('EN', 'EN'), ('CE', 'CE'), ('MCA', 'MCA'),
            ('Other', 'Other')]


class StudentForm(forms.ModelForm):
    roll_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Admission Number'}), required=True, max_length=15)
    college_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'College Name', 'value': 'ABES Engineering College'}),
        required=True, max_length=200)
    branch = forms.CharField(
        label='BRANCHES', widget=forms.Select(choices=BRANCHES, attrs={'class': 'form-control'}), required=True)
    batch_start = forms.CharField(
        label='BATCH START', widget=forms.Select(choices=BATCH_START, attrs={'class': 'form-control'}), required=True)
    batch_end = forms.CharField(
        label='BATCH END', widget=forms.Select(choices=BATCH_END, attrs={'class': 'form-control'}), required=True)
    number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile Number', 'pattern': "[6789][0-9]{9}"}), required=True,
        max_length=10)

    class Meta:
        model = StudentRecord
        fields = ['roll_no', 'college_name', 'branch', 'batch_start', 'batch_end', 'number']

    def clean_roll_no(self):
        roll_no = None
        try:
            roll_no = self.cleaned_data['roll_no']
            StudentRecord.objects.get(roll_no=roll_no.upper())
            raise forms.ValidationError("Roll Number already taken. Contact to us")
        except ObjectDoesNotExist:
            return roll_no.upper()
