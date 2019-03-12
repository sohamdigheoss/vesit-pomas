from django.contrib import admin

from profiles.models import (
    MyUser,
    Domain,
    Student,
    Teacher,
    GroupData,
)

admin.site.register(MyUser)
admin.site.register(Student)
admin.site.register(Domain)
admin.site.register(Teacher)
admin.site.register(GroupData)
