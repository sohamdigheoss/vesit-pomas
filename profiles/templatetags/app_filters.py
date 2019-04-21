from django import template
from profiles.models import MyUser, GroupData, Teacher
from django.db.models import Q
from django.template.defaultfilters import stringfilter

register = template.Library()


@stringfilter
def disp(value,arg):
    users = MyUser.objects.filter(Q(groups__name=arg),Q(is_teacher=True))
    # users=list(users)
    return users
register.filter('disp', disp)

@stringfilter
def group_domain(value,arg):
    domain = GroupData.objects.filter(Q(domain__name=arg))
    return domain
register.filter('group_domain',group_domain)

@stringfilter
def teacher_domain(value,arg):
    domain = Teacher.objects.filter(Q(domain__name=arg))
    return domain
register.filter('teacher_domain',teacher_domain)
