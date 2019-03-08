from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib import messages

from profiles.forms import StudentForm
from profiles.models import MyUser


class HomeView(TemplateView):
    template_name = "home.html"


class StudentSignUpView(CreateView):
    form_class = StudentForm
    model = MyUser
    template_name = 'profiles/form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('home')
