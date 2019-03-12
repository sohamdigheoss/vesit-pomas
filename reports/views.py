from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from .models import Report
from datetime import datetime
#import pdfkit

# Create your views here.
#def transcript_html(request,group_id):

#def transcript(request,group_id):
#    current_user = request.user
#    current_user_groups = request.user.groups.all()
#    group = Group.objects.get(id=group_id)
#    if (current_user.is_teacher and group in current_user_groups):
#        reports = Report.objects.filter(group_id=group_id)
#        context = {
#            'reports': reports
#        }
#        return render(request,'reports/reports.html',context)
#    else:
#        return redirect('home')



def reports(request,group_id):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    group = Group.objects.get(id=group_id)
    if (current_user.is_teacher and group in current_user_groups):
        reports = Report.objects.filter(group_id_id=group_id)
        context = {
            'reports': reports
        }
        return render(request,'reports/reports.html',context)
    else:
        return redirect('home')


def create(request):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    if (current_user.is_teacher):
        if (request.method == 'POST'):
            group_id = request.POST['group_id']
            group = Group.objects.get(id=group_id)
            if (group in current_user_groups):
                print('teacher in group')
                remark = request.POST['remark']
                rating = request.POST['rating']
                report = Report(group_id=group,remark=remark,rating=rating)
                report.save()
                return render(request,'reports/create.html')
            else:
                print('teacher not in group')
                return render(request,'reports/create.html')
        else:
            print('user a teacher, GET')
            return render(request,'reports/create.html')
    else:
        print('user not teacher')
        return redirect('home')


def delete(request):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    if (current_user.is_teacher):
        report = Report.objects.get(id=request.POST['id'])
        group = report.group_id
        report.delete()
        return redirect('reports/reports/'+str(group.id))
    else:
        return redirect('home')
       

def update(request):
    current_user = request.user
    current_user_groups = request.user.groups.all()
    if (current_user.is_teacher):
        report_id = request.POST['id']
        report = Report.objects.get(id=report_id)
        group = report.group_id
        remark = request.POST['remark']
        rating = request.POST['rating']
        report = Report(id=report_id,group_id_id=group,remark=remark,rating=rating)
        report.save()
        print('report saved')
        return redirect('/reports/reports/'+str(group.id))
    else:
        return redirect('home')
 

#def transcript_pdf(request,group_id):
#    project_url = request.get_host()+'/reports/transcript/'+group_id
#    pdf = pdfkit.from_url(project_url,False)
#    response = HttpResponse(pdf,content_type='application/pdf')
#    response['Content-Disposition'] = 'attachment;filename="transcript.pdf"'
#    return response