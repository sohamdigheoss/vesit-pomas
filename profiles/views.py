from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, CreateView
from django.conf import settings

from profiles.forms import StudentMultiForm, DomainForm, TeacherForm
from profiles.models import Teacher
from profiles.tokens import account_activation_token

User = settings.AUTH_USER_MODEL

class HomeView(TemplateView):
    template_name = "home.html"


class StudentSignUpView(CreateView):
    form_class = StudentMultiForm
    template_name = 'profiles/form.html'

    def form_valid(self, form):
        user = form['user'].save()
        profile = form['student'].save(commit=False)
        profile.user = user
        profile.save()
        current_site=get_current_site(self.request)
        subject = 'Activate POMAS account'
        message = render_to_string('./profiles/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        print(user.email_user(subject, message))
        return redirect('account_activation_sent')


def account_activation_sent(request):
    return render(request, './profiles/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(   user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, './profiles/account_activation_invalid.html')


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
