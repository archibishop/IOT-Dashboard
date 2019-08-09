from django.shortcuts import render
from django.views import View
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.
class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard'))
        return render(request, self.template_name, {})

class SignUp(View):
    form_class = SignUpForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = create_user(form)
            login(request, user)
            message_output = 'You have been successfully logged in.'
            messages.success(request, message_output)
            return HttpResponseRedirect(reverse('dashboard'))

        return render(request, self.template_name, {'form': form})


class Login(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                message_output = 'You have successfully Logged In.'
                messages.success(
                    request, message_output)
                return HttpResponseRedirect(reverse('dashboard'))
        message_output = 'User does not exist. Wrong Email/Password.'
        messages.error(request, message_output)
        return render(request, self.template_name, {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        message_output = 'You have logged out of the system.'
        messages.info(
            request, message_output)
        return HttpResponseRedirect(reverse('index'))        

def create_user(form):
    user = User.objects.create_user(username=form.cleaned_data.get(
        'user_name'),
        email=form.cleaned_data.get(
        'email'),
        password=form.cleaned_data.get(
        'password'),
        first_name=form.cleaned_data.get(
        'first_name'),
        last_name=form.cleaned_data.get(
        'last_name'))
    return user          
