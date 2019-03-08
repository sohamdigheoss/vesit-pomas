from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from profiles.models import MyUser, Domain


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = [ProfileInline]
#
#
# admin.site.unregister(User)
admin.site.register(MyUser)
# admin.site.register(Student)
admin.site.register(Domain)
# admin.site.register(Teacher)
