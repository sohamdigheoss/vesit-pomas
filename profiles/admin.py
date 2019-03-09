from django.contrib import admin

from profiles.models import MyUser, Domain, Student, Teacher

admin.site.register(MyUser)
admin.site.register(Student)
admin.site.register(Domain)
admin.site.register(Teacher)
