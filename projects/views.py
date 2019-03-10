from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import Project
#from .models import Project,ProjectGroup
# Create your views here.

#TODO: Authentication required in these methods

def details(request,id):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    project = Project.objects.filter(id=id)
    if (not project.exists()):
        return redirect('home')
    project = project[0]
    if (current_user.is_teacher or project.group in current_user_groups):
        context = {
            'project': project
        }
        return render(request,'projects/details.html',context)
    else:
        return redirect('home')

def create(request):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    if (request.method == 'POST' and current_user.is_student and current_user_groups):
        group = current_user_groups[0]
        name = request.POST['name']
        project = Project.objects.filter(group=group)
        if (project.exists()):
            project = project[0]
            project.name = name
        else:
            project = Project(name=name,group=group)
        project.save()
        return redirect('/projects/create')
    else:
        return render(request,'projects/create.html')

