from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from profiles.models import MyUser, Domain, Student

User = get_user_model()


class StudentForm(UserCreationForm):
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
        ''' Check that the two password entries match'''
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
        if commit:
            user.save()
        return user


