from django import forms
from django.contrib.auth import models, password_validation
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email


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
