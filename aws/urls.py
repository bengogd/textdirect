from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('Showing data/', views.s3file_reader, name="show_data"),
    path('upload form/', views.s3_upload, name='upload'),
]