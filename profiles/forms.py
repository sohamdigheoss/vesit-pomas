from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from betterforms.multiform import MultiModelForm

from profiles.models import MyUser, Domain, Student, Teacher

User = get_user_model()


class UserForm(UserCreationForm):
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'Cellphone', 'class': "form-control"}),
        label='Cellphone number',
        required=True,
        initial='+91')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.is_active = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.phonenumber = self.cleaned_data['phone']
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['division','roll_no']


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name']


class TeacherForm(UserCreationForm):
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'Cellphone', 'class': "form-control"}),
        label='Cellphone number',
        required=True,
        initial='+91')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    domain =  forms.ModelMultipleChoiceField(
        queryset=Domain.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.is_active = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.phonenumber = self.cleaned_data['phone']
        user.set_password(self.cleaned_data["password1"])
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.domain.add(*self.cleaned_data.get('domain'))
        return user

class StudentMultiForm(MultiModelForm):
    form_classes = {
        'user' : UserForm,
        'student' : StudentForm
    }

    @transaction.atomic
    def save(self, commit=True):
        objects = super(StudentMultiForm, self).save(commit=False)
        if commit:
            user = objects['user']
            user.save()
            student = objects['student']
            student.user = user
            student.save()
        return objects