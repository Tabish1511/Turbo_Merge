'''Defines URL patterns for combine_app'''

from django.urls import path
from . import views

app_name = 'merge_app'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),

    #Delete an upload obj
    path('del_upload/<int:upload_id>/', views.del_upload, name='del_upload'),

    # Download Merged PDF
    path('merge_pdf/', views.merge_pdf, name='merge_pdf'),
]