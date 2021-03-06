"""pomas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from machina.app import board
from profiles.views import (
    HomeView,
    StudentSignUpView,
    DomainCreateView,
    TeacherSignUpView,
    account_activation_sent,
    activate,
    GroupCreateView,
    AddMentorView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('register/student',StudentSignUpView.as_view(),name='register'),
    path('register/teacher',TeacherSignUpView.as_view(),name='register/teacher'),
    path('add/domain',DomainCreateView.as_view(),name='domain'),
    path('add/mentor',AddMentorView.as_view(),name='mentor'),
    path('add/group',GroupCreateView.as_view(),name='group'),
    path('account_activation_sent',account_activation_sent,name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
    path('forum/', include(board.urls))
]

urlpatterns+=staticfiles_urlpatterns()