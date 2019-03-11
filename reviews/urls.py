from django.urls import path,include
from . import views
urlpatterns = [
    #path(r'transcript_pdf/<group_id>',views.transcript_pdf,name='transcript_pdf'),
    #path(r'transcript/<group_id>',views.transcript_html,name='transcript_html'),
    path(r'reviews/<group_id>',views.reviews,name='Reviews'),
    path(r'create/',views.create,name='Create'),
    path(r'update/',views.update,name='Update'),
    path(r'delete/',views.delete,name='Delete')
]
