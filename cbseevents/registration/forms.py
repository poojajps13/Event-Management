from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import *

YEAR = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
SEM = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
BRANCHES = [('CSE', 'CSE'), ('IT', 'IT'), ('EC', 'EC'), ('ME', 'ME'), ('EN', 'EN'), ('CE', 'CE'), ('OTHER', 'OTHER'), ]


class StudentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name*'}),
                           required=True, max_length=100)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'abcd@gmail.com',
               'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'}), required=True, max_length=100)
    roll_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Roll No*', 'pattern': "[0-9]{10}"}), required=True,
        max_length=15)
    college_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College Name*'}), required=True,
        max_length=200)
    branch = forms.CharField(label='BRANCHES', widget=forms.Select(choices=BRANCHES, attrs={'class': 'form-control'}),
                             required=True)
    year = forms.CharField(label='YEAR', widget=forms.Select(choices=YEAR, attrs={'class': 'form-control'}),
                           required=True)
    sem = forms.CharField(label='SEMESTER', widget=forms.Select(choices=SEM, attrs={'class': 'form-control'}),
                          required=True)
    number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile Number*', 'pattern': "[789][0-9]{9}"}), required=True,
        max_length=10)

    class Meta:
        model = StudentRecord
        fields = ['name', 'email', 'roll_no', 'college_name', 'branch', 'year', 'sem', 'number']

    def clean_name(self):
        name = self.cleaned_data['name']
        length = len(name)
        if length > 3:
            for i in range(length):
                if ('a' <= name[i] and name[i] <= 'z') or ('A' <= name[i] and name[i] <= 'Z') or name[i] == ' ':
                    pass
                else:
                    raise forms.ValidationError("Invalid Name")
            return name
        return forms.ValidationError("Invalid Name")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except ValidationError:
            return forms.ValidationError("Email is not in correct format")

    def clean_number(self):
        number = self.cleaned_data['number']
        length = len(number)
        if length > 3:
            for i in range(length):
                if ('0' <= number[i] and number[i] <= '9'):
                    pass
                else:
                    raise forms.ValidationError("Invalid Number")
            return number
        return forms.ValidationError("Invalid Number")
