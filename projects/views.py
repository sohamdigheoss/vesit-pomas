from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import Project,ProjectGroup
#from .models import Project,ProjectGroup
# Create your views here.

#TODO: Authentication required in these methods

def details(request,id):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    project_group = ProjectGroup.objects.get(project_id=id)
    if (current_user.is_teacher or project_group in current_user_groups):
        project = Project.objects.get(id=id)
        context = {
            'project': project
        }
        return render(request,'projects/project_profile.html',context)

def create(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        current_user = request.user
        project = Project(name=name)
        project.save()
        return redirect('/projects/create')
    else:
        return render(request,'projects/create_project.html')

