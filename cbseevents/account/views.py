import json
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib import messages, auth
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from events.models import *
from .forms import *


# Create your views here.
# noinspection PyBroadException
class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request):
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
                username = request.POST['user']
                password = request.POST['pass']
                try:
                    User.objects.get(username=username.lower())
                    user = auth.authenticate(username=username.lower(), password=password)
                    if user is not None:
                        auth.login(request, user)
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next'))
                        return redirect("consolidatedview")
                    else:
                        messages.error(request, "Username and password did not match")
                except ObjectDoesNotExist:
                    messages.error(request, "User does not exist")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return render(request, self.template_name, {})
        except Exception:
            messages.error(request, 'Contact Us')
            return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect('home')


# noinspection PyBroadException
def superuser(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "POST":
            try:
                form = SignupForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    User.objects.create_user(username=username.lower(), email=email.lower(), password=password,
                                             first_name=first_name, last_name=last_name)
                    messages.success(request, 'User Created')
                else:
                    messages.error(request, 'Invalid Inputs')
            except Exception:
                messages.warning(request, 'User name and already exits')
        form = SignupForm()
        user = User.objects.all()
        return render(request, 'superuser.html', {'u': user, 'form': form})
    else:
        raise PermissionDenied


def edit_user(request, username):
    try:
        u = User.objects.get(username=username)
        if request.user.is_staff:
            if request.method == "POST":
                u.Username = request.POST['username']
                u.first_name = request.POST['first_name']
                u.last_name = request.POST['last_name']
                u.email = request.POST['email']
                new_password = request.POST['password']
                u.set_password(new_password)
                u.save(update_fields=['username', 'password','first_name','last_name','email'])
            return render(request, 'edit_user.html', {'u': u})
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        messages.error(request, 'Edit not allowed!!!')
    except PermissionDenied:
        messages.error(request, 'User does not exist !!!')
    return render(request, 'edit_user.html', {'u': u})


def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")
    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'superuser.html')
    except Exception as e:
        return render(request, 'superuser.html', {'err': e.message})
    return redirect('superuser')


def consolidated(request, username):
    user = User.objects.get(username=username)
    workshop = WorkshopRecord.objects.filter(user=user)
    seminar = SeminarRecord.objects.filter(user=user)
    training = TrainingRecord.objects.filter(user=user)
    competition = CompetitionRecord.objects.filter(user=user)
    guest_lecture = GuestLectureRecord.objects.filter(user=user)
    print(workshop, seminar, training, competition, guest_lecture)
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
