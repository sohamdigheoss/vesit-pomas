from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView
from django.contrib.auth.models import Group

from profiles.forms import StudentMultiForm, DomainForm, TeacherForm, GroupCreateForm, AddMentorForm
from profiles.models import Teacher, MyUser, GroupData, Domain
from profiles.tokens import account_activation_token


class HomeView(TemplateView):
    template_name = "./index.html"


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
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
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
        current_site = get_current_site(self.request)
        subject = 'Activate POMAS account'
        message = render_to_string('./profiles/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        print(user.email_user(subject, message))
        return redirect('account_activation_sent')


class DomainCreateView(CreateView):
    form_class = DomainForm
    template_name = 'profiles/form.html'
    success_url = reverse_lazy('home')


class GroupCreateView(CreateView):
    form_class = GroupCreateForm
    template_name = './profiles/form.html'
    success_url = reverse_lazy('home')

# class AdminListView(ListView):
#     template_name = ''
#
#     def get_queryset(self):
#         q=Teacher.objects.
#         qs1=Domain.objects.all()
#         grp=[]
#         i=0
#         j=1
#         for q in qs1:
#             grp[i]=Teacher.objects.filter(domain__name=q)
#             grp[j]=GroupData.objects.filter(domain__name=q)
#             i+=2
#             j+=2

class AddMentorView(FormView):
    template_name = './profiles/form.html'
    form_class = AddMentorForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        usr=form.save()
        return redirect('home')


