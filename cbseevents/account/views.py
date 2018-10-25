import json
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView

from events.models import *
from .forms import *
from .tokens import account_activation_token, password_reset_token


# Create your views here.
# noinspection PyBroadException
class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        form1 = EmailForm1()
        form2 = EmailForm2()
        return render(request, self.template_name, {'form': form, 'form1': form1, 'form2': form2})

    def post(self, request):
        try:
            form = LoginForm(request.POST)
            form1 = EmailForm1(request.POST)
            form2 = EmailForm2(request.POST)
            if form.is_valid():
                ''' Begin reCAPTCHA validation '''
                re_captcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': re_captcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                ''' End reCAPTCHA validation '''
                if result['success']:
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    try:
                        u = User.objects.get(username=email.lower())
                        user = auth.authenticate(username=email.lower(), password=password)
                        if user is not None:
                            auth.login(request, user)
                            if 'next' in request.POST:
                                return redirect(request.POST.get('next'))
                            if u.is_staff:
                                return redirect("consolidatedview")
                            return redirect('home')
                        elif not u.is_active:
                            messages.warning(request, 'Please confirm the activation link from your Email')
                        else:
                            messages.error(request, "Email or password did not match")
                    except ObjectDoesNotExist:
                        messages.error(request, "Email or password did not match...")
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            elif form1.is_valid():
                email = form1.cleaned_data['email1']
                try:
                    user = User.objects.get(username=email.lower())
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your Conference Account.'
                        message = render_to_string('acc_active_email.txt', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                            'token': account_activation_token.make_token(user),
                        })
                        email = EmailMessage(mail_subject, message, to=[user.email])
                        email.send()
                        messages.success(request, 'Check Your Email. Activation Link Resend')
                    else:
                        messages.warning(request, 'Your Account is already Activated')
                except ObjectDoesNotExist:
                    messages.error(request, 'Invalid Email. Try Again')
            elif form2.is_valid():
                email = form2.cleaned_data['email2']
                try:
                    user = User.objects.get(username=email.lower())
                    if user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Password Reset link of your Conference Account.'
                        message = render_to_string('forget-password.txt', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.email)).decode(),
                            'token': password_reset_token.make_token(user),
                        })
                        email = EmailMessage(mail_subject, message, to=[user.email])
                        email.send()
                        messages.success(request, 'Check Your Email. Password Reset Link Send')
                    else:
                        messages.warning(request, 'Activate your Account')
                except ObjectDoesNotExist:
                    messages.error(request, 'Invalid Email. Try Again')
            else:
                messages.warning(request, "Invalid Input. Please try again")
        except Exception:
            messages.error(request, 'Please Try again after some time')
        form = LoginForm()
        form1 = EmailForm1()
        form2 = EmailForm2()
        return render(request, self.template_name, {'form': form, 'form1': form1, 'form2': form2})


# noinspection PyBroadException
class Signup(TemplateView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form1 = SignupForm()
        form2 = StudentForm()
        return render(request, self.template_name, {'form1': form1, 'form2': form2})

    def post(self, request):
        form1 = SignupForm(request.POST)
        form2 = StudentForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            try:
                ''' Begin reCAPTCHA validation '''
                re_captcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': re_captcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                ''' End reCAPTCHA validation '''
                if result['success']:
                    username = form1.cleaned_data['email']
                    first_name = form1.cleaned_data['first_name']
                    last_name = form1.cleaned_data['last_name']
                    email = form1.cleaned_data['email']
                    password = form1.cleaned_data['password']
                    user = User.objects.create_user(username=username.lower(), email=email.lower(), password=password,
                                                    first_name=first_name, last_name=last_name, is_active=False)
                    temp = form2.save(commit=False)
                    temp.user = user
                    temp.save()
                    '''Begin Email Sending '''
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your Conference Account.'
                    message = render_to_string('acc_active_email.txt', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user),
                    })
                    email = EmailMessage(mail_subject, message, to=[user.email])
                    email.send()
                    '''End Email sending'''
                    messages.success(request, 'Please confirm your email address to complete the registration.')
                    return redirect("login")
                else:
                    messages.error(request, "Invalid reCAPTCHA. Please try again.")
            except Exception:
                messages.error(request, 'Problem to Sending Email. Please Contact Us.')
                return redirect("signup")
        else:
            messages.error(request, "Invalid Input. Please try again")
        return render(request, self.template_name, {'form1': form1, 'form2': form2})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.success(request, 'Thank you for Email Confirmation.')
        return redirect("home")
    elif user.is_active:
        auth.login(request, user)
        return redirect("home")
    else:
        messages.error(request, 'Activation link is invalid! Contact to Us')
        return redirect("account:signup")


def logout(request):
    auth.logout(request)
    return redirect('home')


# noinspection PyBroadException
class ResetPassword(TemplateView):
    template_name = 'reset-password.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(email=uid)
            if user.is_active and password_reset_token.check_token(user, kwargs['token']):
                form = ResetPasswordForm()
                return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'Invalid Link')
        return redirect('home')

    def post(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(email=uid)
            if user.is_active and password_reset_token.check_token(user, kwargs['token']):
                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password Updated')
                    auth.login(request, user)
                    return redirect('home')
                messages.error(request, 'Password Does not Match')
                return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'Invalid Link')
        return redirect('home')


# noinspection PyBroadException
def superuser(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                form = SignupForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    User.objects.create_user(username=username.lower(), email=email.lower(), password=password,
                                             first_name=first_name, last_name=last_name, is_active=True, is_staff=True)
                    messages.success(request, 'User Created')
                else:
                    messages.error(request, 'Invalid Inputs')
            except Exception:
                messages.warning(request, 'User name and already exits')
        form = SignupForm()
        user = User.objects.filter(is_staff=True)
        return render(request, 'superuser.html', {'u': user, 'form': form})
    else:
        raise PermissionDenied


def edit_user(request, username):
    try:
        u = User.objects.get(username=username)
        if request.user.is_superuser:
            if request.method == "POST":
                form = EditUserForm(request.POST, instance=u)
                if form.is_valid():
                    u.first_name = form.cleaned_data['first_name']
                    u.last_name = form.cleaned_data['last_name']
                    u.email = form.cleaned_data['email']
                    new_password = form.cleaned_data['password']
                    u.set_password(new_password)
                    u.save(update_fields=['username', 'password', 'first_name', 'last_name', 'email'])
                    messages.success(request, 'Updated')
                else:
                    messages.info(request, 'Invalid Input')
            form = EditUserForm(instance=u)
            return render(request, 'edit_user.html', {'form': form})
        else:
            raise PermissionDenied
    except PermissionDenied:
        messages.error(request, 'Edit not allowed!!!')
    except ObjectDoesNotExist:
        messages.error(request, 'User does not exist !!!')
    return redirect('superuser')


def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")
    except ObjectDoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'superuser.html')
    except Exception as e:
        return render(request, 'superuser.html', {'err': e})
    return redirect('superuser')


def consolidated(request, username):
    user = User.objects.get(username=username)
    workshop = WorkshopRecord.objects.filter(user=user)
    seminar = SeminarRecord.objects.filter(user=user)
    training = TrainingRecord.objects.filter(user=user)
    competition = CompetitionRecord.objects.filter(user=user)
    guest_lecture = GuestLectureRecord.objects.filter(user=user)
    return render(request, 'consolidatedview.html',
                  {'workshop': workshop, 'training': training, 'competition': competition,
                   'seminar': seminar, 'guest_lecture': guest_lecture, 'now': timezone.now()})


def consolidatedview(request):
    workshop = WorkshopRecord.objects.filter(user=request.user)
    seminar = SeminarRecord.objects.filter(user=request.user)
    training = TrainingRecord.objects.filter(user=request.user)
    competition = CompetitionRecord.objects.filter(user=request.user)
    guest_lecture = GuestLectureRecord.objects.filter(user=request.user)
    return render(request, 'consolidatedview.html',
                  {'workshop': workshop, 'training': training, 'competition': competition,
                   'seminar': seminar, 'guest_lecture': guest_lecture, 'now': timezone.now()})
