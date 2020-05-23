from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView


from accounts.forms import SignUpForm
from .models import User
from .forms import LoginForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        form = self.get_form()
        user = User.objects.get(username=form.data.get('username'))

        login(self.request, user)
        return redirect('events:event_list')


class AccountDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class LogoutView(LogoutView):
    template_name = 'accounts/top.html'
