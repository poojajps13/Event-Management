from django import forms
from django.contrib.auth import models, password_validation
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email

from student.models import StudentRecord

BATCH_START = [('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'),
               ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')]
BATCH_END = [('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'),
             ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')]
BRANCHES = [('CSE', 'CSE'), ('IT', 'IT'), ('EC', 'EC'), ('ME', 'ME'), ('EN', 'EN'), ('CE', 'CE'), ('MCA', 'MCA'),
            ('Other', 'Other')]


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=True,
        max_length=20)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False,
        max_length=30)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'}),
        required=True, max_length=40)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'pattern': "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"}),
        required=True, max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password'}), required=True, max_length=30)

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean_email(self):
        email = None
        try:
            email = self.cleaned_data['email']
            validate_email(email)
            user = models.User.objects.get(email=email.lower())
            if user.is_active:
                raise forms.ValidationError("This Email Address is already used")
        except ObjectDoesNotExist:
            pass
        return email

    def clean_confirm_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']
        if password1 != password2:
            raise forms.ValidationError("Password does not match")
        else:
            password_validation.validate_password(password2)
        return password2


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


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}), required=True, max_length=40)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True, max_length=30)


class EmailForm(forms.Form):
    email1 = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control col-sm-8 mb-2 mr-3', 'placeholder': 'Email',
               'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'}), required=True, max_length=40)

    def clean_email1(self):
        try:
            email = self.cleaned_data['email1']
            validate_email(email)
            return email.lower()
        except ValidationError:
            return forms.ValidationError("Email is not in correct format")


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Password', 'pattern': "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
               'title': 'New Password'}), required=True, max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password', 'title': 'Re-Enter Password',
               'pattern': "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"}), required=True, max_length=20)

    def clean_confirm_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']
        if password1 != password2:
            raise forms.ValidationError("Password does not match")
        else:
            password_validation.validate_password(password2)
        return password2


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=True, max_length=20)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False, max_length=30)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email',
               'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'}), required=True, max_length=40)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'pattern': "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"}),
        required=True, max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password',
               'pattern': "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"}), required=True, max_length=30)

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'password']
