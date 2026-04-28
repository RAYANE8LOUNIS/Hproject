# Student 5 - Reports (PDF/Excel) URL routes.

from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pdf/', views.download_pdf, name='download_pdf'),
    path('excel/', views.download_excel, name='download_excel'),
]
