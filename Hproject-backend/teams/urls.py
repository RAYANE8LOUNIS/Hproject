from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
]