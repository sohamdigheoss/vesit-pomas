from django.urls import path,include
from . import views
urlpatterns = [
    path(r'details/<id>',views.details,name='Details'),
    path(r'create',views.create,name='Create') 
]
