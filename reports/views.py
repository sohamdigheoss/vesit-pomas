from django.shortcuts import render
from django.http import HttpResponse
from .models import Report
import pdfkit

# Create your views here.
def transcript_html(request,group_id):
    reports = Report.objects.filter(group_id_id=group_id)
    context = {
        'reports': reports
    }
    return render(request,'reports/transcript.html',context)

def transcript_pdf(request,group_id):
    project_url = request.get_host()+'/reports/transcript/'+group_id
    pdf = pdfkit.from_url(project_url,False)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="transcript.pdf"'
    return response
