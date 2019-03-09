from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib import messages

from profiles.forms import StudentMultiForm, DomainForm, TeacherForm
from profiles.models import Teacher


class HomeView(TemplateView):
    template_name = "home.html"


class StudentSignUpView(CreateView):
    form_class = StudentMultiForm
    template_name = 'profiles/form.html'
    success_url = reverse_lazy('home')


class TeacherSignUpView(CreateView):
    form_class = TeacherForm
    template_name = 'profiles/form.html'
    model = Teacher

    def get_context_data(self, **kwargs):
        kwargs['user-type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class DomainCreateView(CreateView):
    form_class = DomainForm
    template_name = 'profiles/form.html'
    success_url = reverse_lazy('home')
