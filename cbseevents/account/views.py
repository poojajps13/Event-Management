

import json
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Create your views here.
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
                        return redirect("home")
                    else:
                        messages.error(request, "Username and password did not match")
                except ObjectDoesNotExist:
                    messages.error(request, "User does not exist")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        except ObjectDoesNotExist:
            messages.error(request, 'Contact Us')
            return redirect("account:login")
        return render(request, self.template_name, {})