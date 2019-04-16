from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from betterforms.multiform import MultiModelForm

from profiles.models import MyUser, Domain, Student, Teacher, GroupData

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
        fields = ('first_name', 'last_name', 'email')

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
        user.is_active = False
        user.username,_ = self.cleaned_data['email'].split('@')
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
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.is_active = False
        user.username,_ = self.cleaned_data['email'].split('@')
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.phonenumber = self.cleaned_data['phone']
        user.set_password(self.cleaned_data["password1"])
        user.save()
        new_group, created = Group.objects.get_or_create(name='teachers')
        new_group.user_set.add(user)
        # ne, created = Group.objects.get_or_create(name='multiple')
        # ne.user_set.add(user)
        teacher = Teacher.objects.create(user=user)
        teacher.domain.add(*self.cleaned_data.get('domain'))
        return user


class StudentMultiForm(MultiModelForm):
    form_classes = {
        'user' : UserForm,
        'student' : StudentForm
    }


class GroupCreateForm(forms.ModelForm):
    user1 = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_student=True), empty_label="(Choose a User)")
    user2 = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_student=True), empty_label="(Choose a User)")
    user3 = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_student=True), empty_label="(Choose a User)")
    user4 = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_student=True), empty_label="(Choose a User)")
    domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(),
        required=True,
        empty_label="(Choose a Domain)"
    )
    class Meta:
        model = Group
        fields = ['name']

    def save(self):
        new_group, created = Group.objects.get_or_create(name=self.cleaned_data['name'])
        new_group.user_set.add(self.cleaned_data['user1'])
        new_group.user_set.add(self.cleaned_data['user2'])
        new_group.user_set.add(self.cleaned_data['user3'])
        new_group.user_set.add(self.cleaned_data['user4'])
        group=GroupData.objects.create(group=new_group)
        group.domain.add(self.cleaned_data.get('domain'))
        return new_group

class AddMentorForm(forms.Form):
    mentor = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_teacher=True), empty_label="(Choose a User)")
    name  = forms.ModelChoiceField(queryset=Group.objects.all(),empty_label='(choose group)')

    def save(self):
        user = MyUser.objects.get(username__iexact=self.cleaned_data['mentor'])
        new_group= Group.objects.get(name=self.cleaned_data['name'])
        user.groups.add(new_group)
        return user